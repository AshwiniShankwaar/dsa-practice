"""Deep agents for the DSA practice tool.

Public API (re-exported by agents/__init__.py):
- generate_test_case: one-shot test suite generation for a question.
- evaluate_solution: multi-turn mentor review of the user's solution.
- generate_readme_section: one-shot README section for a solved question.
"""
import json
import os
import queue
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout

from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage

from agents.config import Config
from agents.prompt import BASE_PROMPT_TEMPLATE, TEST_CASE_GENERATE, README_UPDATE
from agents.tools import json_validator, save_in_test_file, save_learning_file
from utils.load_files import _load_testCase
from utils.logger import get_logger

logger = get_logger(__name__)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The mentor's long-term memory of the user's coding patterns, kept across questions.
KB_FILE = Config.kb_file

# Shared chat model for every agent (OpenRouter via env config).
model = init_chat_model(
    model=Config.model,
    model_provider=Config.model_provider,
    api_key=Config.model_api_key,
    temperature=Config.model_temperature,
)


def _create_agent(name: str, prompt, tools: list = [], backend=None):
    """Build a compiled deepagents graph with the shared model."""
    return create_deep_agent(
        model=model,
        name=name,
        tools=tools,
        system_prompt=prompt,
        backend=backend,
    )


def _text(message) -> str:
    """Extract plain text from a message whose content may be a str or block list."""
    content = message.content
    if isinstance(content, str):
        return content
    # Content blocks: join the text parts.
    return "".join(
        b.get("text", "") if isinstance(b, dict) else str(b) for b in content
    )


# never wait on the evaluation agent (or a follow-up question) longer than this
EVAL_TIMEOUT_SECONDS = Config.eval_timeout_seconds


def _invoke_with_timeout(agent, payload):
    """Run agent.invoke in a worker thread and give up after EVAL_TIMEOUT_SECONDS.

    Windows has no SIGALRM, so a thread + future timeout is the portable cap.
    ponytail: the worker thread keeps running after a timeout (we just stop
    waiting); switch to client-level timeouts if orphaned requests become a problem.
    """
    pool = ThreadPoolExecutor(max_workers=1)
    try:
        return pool.submit(agent.invoke, payload).result(timeout=EVAL_TIMEOUT_SECONDS)
    except FutureTimeout:
        raise TimeoutError(f"Evaluation agent timed out after {EVAL_TIMEOUT_SECONDS}s")
    finally:
        pool.shutdown(wait=False, cancel_futures=True)


def _timed_input(prompt: str):
    """input() capped at EVAL_TIMEOUT_SECONDS.

    Returns the typed line, "" on EOF (non-interactive run), or None on timeout.
    ponytail: the daemon reader thread stays blocked on input() after a timeout;
    harmless because the process ends right after the evaluation session.
    """
    q = queue.Queue()

    def _read():
        try:
            q.put(input(prompt))
        except EOFError:
            q.put("")

    threading.Thread(target=_read, daemon=True).start()
    try:
        return q.get(timeout=EVAL_TIMEOUT_SECONDS)
    except queue.Empty:
        return None


def _json_from_text(text: str):
    """Best-effort: parse the outermost {...} block in a model reply, else None."""
    s, e = text.find("{"), text.rfind("}")
    if s == -1 or e <= s:
        return None
    try:
        return json.loads(text[s:e + 1])
    except json.JSONDecodeError:
        return None


def generate_test_case(question_id, question_type, question_description,
                       question_example, question_hints, test_cases_path) -> str:
    """One-shot: generate and save test cases for a question.

    The agent validates its JSON with json_validator and persists it via
    save_in_test_file. Returns the agent's final message content.
    """
    agent = _create_agent(
        "Test_case_generator",
        TEST_CASE_GENERATE.format(
            problem_type=question_type,
            problem_description=question_description,
            examples=question_example,
            hints=question_hints,
            metadata={
                "question_id": question_id,
                "test_cases_path": test_cases_path,
            },
        ),
        [json_validator, save_in_test_file],
    )

    # count before/after so we can tell whether the agent actually saved to disk
    question_dir = os.path.basename(os.path.normpath(test_cases_path))
    before = len(_load_testCase(question_dir))

    result = agent.invoke(
        input={
            "messages": [
                HumanMessage(
                    content=f"Write test cases for the question: {question_description}, "
                            f"also provide expected outputs."
                )
            ]
        }
    )
    reply = _text(result["messages"][-1])

    # visibility into silent runs: which tools did the model actually call?
    for m in result["messages"]:
        calls = getattr(m, "tool_calls", None)
        if calls:
            logger.info("Test generator called tools: %s", [c["name"] for c in calls])

    # Fallback: some models reply with raw JSON (or write to the agent's
    # in-memory filesystem) instead of calling save_in_test_file — salvage it.
    after = len(_load_testCase(question_dir, force_reload=True))
    if after <= before:
        parsed = _json_from_text(reply)
        tests = parsed.get("tests", parsed) if isinstance(parsed, dict) else None
        if tests:
            logger.warning("Agent did not save; salvaging %d cases from its reply.", len(tests))
            save_in_test_file.func(tests, test_cases_path)
        else:
            logger.warning("Test generator produced no savable test cases.")
    return reply


def evaluate_solution(question_info: dict, solution_code: str, rerun=None) -> dict:
    """Evaluate the user's solution with a mentor agent.

    This agent is responsible to evaluate the solution built for the question:
    correctness/edge cases, time & space complexity, optimization strategy and
    pythonic style — it mentors and NEVER outputs complete solution code.
    It has multi-turn ability: after printing the first evaluation it loops on
    console input() so the user can ask follow-up questions (empty input or
    'exit'/'quit' ends the loop). If the user seems unclear on the topic it
    writes/refreshes a learning file via the save_learning_file tool. It also
    maintains a coding-pattern knowledge base (kb/coding_patterns.md) that it
    refreshes each session and uses to answer "how can I improve" questions.

    :param question_info: tracker entry (question_id, question_name, url, type,
                          description, examples, hints, attempts).
    :param solution_code: the user's solution source code.
    :param rerun: optional zero-arg callable returning
                  (elapsed, test_summary, outcome, failed_cases); exposed to
                  the agent as the rerun_solution tool so the user can say
                  "rerun it" after editing their solution mid-session.
    :return: {"approved": bool, "feedback": <first response text>}
    """
    question_id = question_info.get("question_id")
    question_dir = question_info.get("dir", f"s{question_id}")
    tools = [save_learning_file]

    if rerun is not None:
        @tool
        def rerun_solution() -> str:
            """Re-run the user's CURRENT solution file against all saved test
            cases (fresh import, so edits made since the session started are
            picked up). Returns the test results plus the current solution
            source code. Call this ONLY when the user asks to rerun/retest."""
            try:
                elapsed, summary, outcome, failed_cases = rerun()
                code = ""
                try:
                    solution_file = os.path.join(REPO_ROOT, "solutions", question_dir, "solution.py")
                    with open(solution_file, encoding="utf-8") as f:
                        code = f.read()
                except OSError as e:
                    code = f"(could not read solution file: {e})"
                return json.dumps({
                    "outcome": outcome,
                    "test_summary": summary,
                    "failed_cases": failed_cases,
                    "time_seconds": round(elapsed, 4),
                    "current_solution_code": code,
                })
            except Exception as e:
                return f"ERROR while rerunning the solution: {e}"

        tools.append(rerun_solution)

    agent = _create_agent(
        "Solution_evaluator",
        BASE_PROMPT_TEMPLATE,
        tools,
    )

    # current coding-pattern KB (if any) goes into the context so the agent
    # can merge new observations instead of starting from scratch
    kb_content = ""
    if os.path.exists(KB_FILE):
        try:
            with open(KB_FILE, encoding="utf-8") as f:
                kb_content = f.read()
        except OSError:
            logger.warning("Could not read coding KB at %s", KB_FILE, exc_info=True)

    # All the review context goes into the first user message.
    context = {
        "question_id": question_id,
        "question_name": question_info.get("question_name"),
        "url": question_info.get("url"),
        "type": question_info.get("type"),
        "description": question_info.get("description"),
        "examples": question_info.get("examples"),
        "hints": question_info.get("hints"),
        "previous_attempts": len(question_info.get("attempts", [])),
        # learning notes live next to the solution: solutions/<dir>/learning.md
        "learning_file_path": f"solutions/{question_dir}/learning.md",
        "kb_file_path": KB_FILE,
        "coding_pattern_kb": kb_content or "(empty — first evaluation session)",
    }
    first_message = HumanMessage(
        content=f"Question context:\n{json.dumps(context, indent=2, default=str)}\n\n"
                f"My solution code:\n```python\n{solution_code}\n```\n\n"
                f"Please evaluate my solution."
    )

    result = _invoke_with_timeout(agent, {"messages": [first_message]})
    feedback = _text(result["messages"][-1])
    approved = "VERDICT: APPROVED" in feedback
    print(feedback)

    # Follow-up loop: keep the full message history so the agent has context.
    messages = list(result["messages"])
    while True:
        user_input = _timed_input("\nAsk a follow-up (empty/exit/quit to finish): ")
        if user_input is None:
            print(f"\n(no follow-up within {EVAL_TIMEOUT_SECONDS}s — ending the attempt)")
            break
        user_input = user_input.strip()
        if not user_input or user_input.lower() in ("exit", "quit"):
            break
        messages.append(HumanMessage(content=user_input))
        try:
            result = _invoke_with_timeout(agent, {"messages": messages})
        except TimeoutError:
            print(f"(mentor took longer than {EVAL_TIMEOUT_SECONDS}s to answer — ending the session)")
            break
        messages = list(result["messages"])
        print(_text(messages[-1]))

    return {"approved": approved, "feedback": feedback}


def generate_readme_section(question_info: dict, solution_code: str,
                            existing_section: str | None = None) -> str:
    """One-shot: produce the markdown README section for one solved question.

    Returns ONLY the section text (heading, approach, complexity). If
    existing_section is given the agent updates it instead of duplicating.
    """
    agent = _create_agent("Readme_writer", README_UPDATE)

    info = {
        "question_id": question_info.get("question_id"),
        "question_name": question_info.get("question_name"),
        "url": question_info.get("url"),
        "type": question_info.get("type"),
        "description": question_info.get("description"),
    }
    parts = [
        f"Question info:\n{json.dumps(info, indent=2, default=str)}",
        f"My accepted solution:\n```python\n{solution_code}\n```",
    ]
    if existing_section:
        parts.append(f"Existing README section to update:\n{existing_section}")
    parts.append("Write the markdown section for this question.")

    result = agent.invoke(
        input={"messages": [HumanMessage(content="\n\n".join(parts))]}
    )
    return _text(result["messages"][-1])
