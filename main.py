import json
import sys

import time
import uuid
import os
from pathlib import Path
from utils.question_details import get_question_details,move_file,slug_from_url
from agents import generate_test_case, evaluate_solution, generate_readme_section
from agents.config import Config
from utils.load_files import _load_solution,_load_testCase
from utils.readme import get_readme_section, upsert_readme_section
from utils.logger import get_logger
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logger = get_logger(__name__)

class Tracker:
    """Thin JSON-file store for question metadata and attempt history."""
    FILE_NAME = Config.tracker_file
    @staticmethod
    def load():
        """Load the tracker file, creating an empty one if it doesn't exist."""
        if not os.path.exists(Tracker.FILE_NAME):
            logger.info("Tracker file not found; creating %s", Tracker.FILE_NAME)
            Tracker.save({})
            return {}
        try:
            with open(Tracker.FILE_NAME, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Tracker file is empty or corrupted. Starting a new tracker.")
            return {}
    @staticmethod
    def save(data):
        """Persist the tracker dict to disk (creating parent dirs if configured)."""
        parent = os.path.dirname(Tracker.FILE_NAME)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(Tracker.FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)


def execute_solution(solution, test_case):
    """
    Executes the solution depending on input type.
    """
    if isinstance(test_case, tuple):
        return solution._run(*test_case)
    if isinstance(test_case, dict):
        return solution._run(**test_case)
    return solution._run(test_case)



def main(question_dir: str, question_type: str, force_reload: bool = False):
    """
    Runs all test cases for the given question. question_dir is the leetcode
    slug with '-' -> '_' (files live at solutions/<dir>/solution.py and
    testCases/<dir>/testcase.py). force_reload re-imports both files so a
    rerun picks up edits made since the process started.
    """
    logger.info(f"Running Question {question_dir} ({question_type})")
    try:
        solution = _load_solution(question_dir, force_reload)
        test_cases = _load_testCase(question_dir, force_reload)
        logger.info("Solution Loaded Successfully")
        start = time.perf_counter()
        test_summary = {
            "Pass": 0,
            "Fail": 0,
            "Error": 0  # exceptions raised by the solution, as opposed to wrong answers
        }
        failed_cases = []
        for test_name, value in test_cases.items():
            test_input = value[0]
            expected = value[1]
            try:
                actual = execute_solution(solution, test_input)
                if actual == expected:
                    logger.info("%s : PASSED", test_name)
                    test_summary["Pass"] += 1
                else:
                    logger.error("%s : FAILED", test_name)
                    logger.error("Expected : %s", expected)
                    logger.error("Actual   : %s", actual)
                    failed_cases.append(test_name)
                    test_summary["Fail"] += 1
            except Exception as ex:
                logger.exception("Exception while executing %s", test_name)
                failed_cases.append(test_name)
                test_summary["Fail"] += 1
                test_summary["Error"] += 1
        end = time.perf_counter()
        return (
            end - start,
            test_summary,
            "Pass" if test_summary["Fail"] == 0 else "Fail",
            failed_cases
        )

    except Exception:
        logger.exception("Unable to execute Question %s", question_dir.replace("_"," ").capitalize())
        raise


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print(
            "python main.py "
            "'{\"question_id\":1,\"url\":\"https://leetcode.com/problems/two-sum\"}'"
        )
        print("Optional key: \"evaluate\": false  -> run tests only, skip the mentor agent")
        sys.exit(1)

    data = json.loads(sys.argv[1].replace("'", '"'))
    # per-run "evaluate" param wins; otherwise the .env default applies
    run_eval = data.get("evaluate", Config.evaluate_by_default)
    # name and type are no longer params: the slug names the files/dirs and
    # leetcode itself provides the official title and topic tags.
    slug = slug_from_url(data["url"])                # e.g. "two-sum"
    question_dir = slug.replace("-", "_")            # e.g. "two_sum" (importable dir name)
    details = get_question_details(data["url"])
    question_name = details.get("title") or slug.replace("-", " ").title()
    if details["screenshot"]:
        # the solution now lives in its own dir, so the screenshot can too
        dest_path = os.path.join(BASE_DIR, f"solutions/{question_dir}/description.png")
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        move_file(dest_path,details["screenshot"])
        details["screenshot"] = dest_path  # tracker stores the final location

    tracker = Tracker.load()
    question_key = str(data["question_id"])  # leetcode ids are unique; no name hash needed
    if question_key not in tracker:
        tracker[question_key] = {
            "question_id": data["question_id"],
            "question_name": question_name,
            "url": data["url"],
            "type": details.get("type", ""),
            "slug": slug,
            "dir": question_dir,
            "description": details["description"],
            "examples": details["examples"],
            "hints": details["hints"],
            "screenshot": details["screenshot"],
            "attempts": []
        }
    # keep entries created before the dir-based layout loadable
    tracker[question_key].setdefault("slug", slug)
    tracker[question_key]["dir"] = question_dir

    # generate test cases via the agent when the file is missing or too thin
    if len(_load_testCase(question_dir)) < Config.min_test_cases:
        try:
            gen_msg = generate_test_case(
                question_id = tracker[question_key].get("question_id"),
                question_type = tracker[question_key].get("type"),
                question_description = tracker[question_key].get("description"),
                question_example = tracker[question_key].get("examples"),
                question_hints = tracker[question_key].get("hints"),
                test_cases_path = f"{BASE_DIR}/testCases/{question_dir}/"
            )
            logger.info("Test case generator: %s", (gen_msg or "")[:300])
            # the agent just wrote the file: force a fresh import in this process
            case_count = len(_load_testCase(question_dir, force_reload=True))
            if case_count < Config.min_test_cases:
                logger.warning("Generation finished but only %d test cases exist.", case_count)
        except Exception:
            logger.warning("Test case generation failed; running with existing cases.", exc_info=True)

    time_taken, test_summary, outcome, failed_cases = main(
        question_dir,
        tracker[question_key].get("type", "")
    )

    # mentor-style review of the solution source (agent reads code, never edits it)
    solution_source = Path(BASE_DIR, f"solutions/{question_dir}/solution.py").read_text(encoding="utf-8")
    evaluation = None
    if test_summary["Error"]:
        # a crashing solution isn't ready for review — record the attempt and exit below
        logger.error("Solution raised exceptions in %d test case(s); skipping evaluation "
                     "(tracebacks above).", test_summary["Error"])
    elif not run_eval:
        # practice mode: run tests only so the mentor can't spoil the approach
        logger.info("Evaluation skipped (\"evaluate\": false in params).")
    else:
        try:
            evaluation = evaluate_solution(
                tracker[question_key],
                solution_source,
                # lets the mentor re-test the (possibly edited) solution on request
                rerun=lambda: main(question_dir, tracker[question_key].get("type", ""),
                                   force_reload=True),
            )
        except Exception:
            logger.warning("Evaluation agent failed; recording attempt without feedback.", exc_info=True)

    attempt = {
        "attempt_id": str(uuid.uuid4()),
        "time_taken": round(time_taken, 4),
        "test": {
            "pass": test_summary["Pass"],
            "fail": test_summary["Fail"],
            "error": test_summary["Error"]
        },
        "failed_cases": failed_cases,
        "outcome": outcome,
        "evaluation": evaluation["feedback"] if evaluation else None,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    tracker[question_key]["attempts"].append(attempt)

    Tracker.save(tracker)

    # publish the approach to the solution-approach journal only when tests
    # pass AND the mentor approves (README stays app documentation)
    if outcome == "Pass" and evaluation and evaluation.get("approved"):
        try:
            qid = data["question_id"]
            existing = get_readme_section(qid, path=Config.solution_approach_file)
            section = generate_readme_section(tracker[question_key], solution_source, existing)
            upsert_readme_section(qid, section, path=Config.solution_approach_file)
            logger.info("Solution approach updated for question %s in %s",
                        qid, Config.solution_approach_file)
        except Exception:
            logger.warning("Solution approach update failed; attempt already recorded.", exc_info=True)
    else:
        logger.info("Solution approach not updated (outcome=%s, approved=%s)",
                    outcome, evaluation.get("approved") if evaluation else "N/A")

    logger.info("=" * 60)
    logger.info("Execution Summary")
    logger.info("Question      : %s", question_name)
    logger.info("Outcome       : %s", outcome)
    logger.info("Time Taken    : %.4f sec", time_taken)
    logger.info("Passed Tests  : %d", test_summary["Pass"])
    logger.info("Failed Tests  : %d", test_summary["Fail"])
    logger.info("Evaluation    : %s",
                ("Approved" if evaluation.get("approved") else "Needs work") if evaluation else "Unavailable")

    if failed_cases:
        logger.info("Failed Cases  : %s", ", ".join(failed_cases))

    logger.info("=" * 60)

    if test_summary["Error"]:
        sys.exit(1)  # solution crashed: exit non-zero after logging everything above