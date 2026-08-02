# DSA Practice App

A personal LeetCode practice environment with an AI mentor. You write the
solution; the app fetches the question, generates a test suite, runs your code
against it, and (optionally) hands the result to a mentor agent that reviews
your approach — without ever giving you the answer. Every attempt is tracked,
and approved solutions get their approach written up automatically.

## How It Works

```
python main.py '{"question_id": 1, "url": "https://leetcode.com/problems/two-sum"}'
        |
        v
1. Fetch question details from LeetCode (GraphQL, Playwright fallback)
2. Generate test cases via agent (if fewer than MIN_TEST_CASES exist)
3. Run your solution against every test case
4. Mentor agent evaluates the solution (unless disabled)
5. Record the attempt in the tracker
6. On Pass + mentor approval: update solution_approach.md
```

## Quick Start

1. Install dependencies (Python 3.13, [uv](https://docs.astral.sh/uv/)):

   ```
   uv sync
   ```

2. Create `.env` at the repo root (see [Configuration](#configuration)) with at
   least your OpenRouter key, model and provider.

3. Add your solution at `solutions/<question_dir>/solution.py`, where
   `question_dir` is the LeetCode URL slug with `-` replaced by `_`
   (e.g. `https://leetcode.com/problems/two-sum` → `solutions/two_sum/solution.py`):

   ```python
   class Solution:
       def _run(self, nums, target):
           # your logic here
           ...
   ```

   `_run` is the harness entry point — keep the name; the parameters must match
   the problem's argument names.

4. Run it:

   ```
   python main.py '{"question_id": 1, "url": "https://leetcode.com/problems/two-sum"}'
   ```

### Run Parameters

The single CLI argument is a JSON object:

| Key           | Required | Meaning                                                        |
|---------------|----------|----------------------------------------------------------------|
| `question_id` | yes      | LeetCode question id (tracker key)                             |
| `url`         | yes      | LeetCode problem URL (slug drives file/dir names)              |
| `evaluate`    | no       | `false` = run tests only, skip the mentor (overrides the .env default) |

Skipping evaluation is useful when you want to struggle with the problem
yourself first — the mentor is good enough at hinting that it can spoil the
learning if you invoke it on every attempt.

## The Agents

All agents run on one model configured in `.env` (OpenRouter via LangChain +
deepagents).

### Test Case Generator (one-shot)
Generates 15–25 test cases per question — standard, boundary, edge and stress
cases — validates them as JSON and saves them to
`testCases/<question_dir>/testcase.py`. Runs automatically whenever a question
has fewer than `MIN_TEST_CASES` cases. If the model replies with raw JSON
instead of calling the save tool, the runner salvages and saves it anyway.

### Solution Evaluator / Mentor (multi-turn)
Reviews your code statically: correctness and edge cases, time/space
complexity, optimization strategy, and Pythonic style. It **never writes the
solution for you** — it mentors through questions, patterns and hints. Its
first reply ends with `VERDICT: APPROVED` or `VERDICT: NEEDS_IMPROVEMENT`.

After the first evaluation you get an interactive follow-up loop in the
terminal (empty input, `exit` or `quit` to finish; the session also ends after
`EVAL_TIMEOUT_SECONDS` without input). During the session the mentor can:

- **Rerun your solution** — say "rerun it" after editing your file; the
  `rerun_solution` tool re-imports your current code, runs the full test
  suite, and continues the discussion on the fresh code.
- **Write learning notes** — if you seem stuck on a concept it writes a
  beginner-friendly explainer to `solutions/<question_dir>/learning.md`.
- **Maintain a coding-pattern knowledge base** — `kb/coding_patterns.md` is
  the mentor's long-term memory of how you code (habits, strengths, recurring
  mistakes, progress). It refreshes it every session, and you can ask it
  "how can I improve?" for personal, KB-backed advice.

### Approach Writer (one-shot)
When your tests pass **and** the mentor approves, this agent writes/updates the
question's section in `solution_approach.md` — your journal of solved questions
and the approach actually used.

## Configuration

All knobs live in `.env` at the repo root and are loaded through
`agents/config.py` (`Config`). Every value has a sane default except the model
credentials.

| Variable                 | Default                | Meaning                                                  |
|--------------------------|------------------------|----------------------------------------------------------|
| `OPEN_ROUTER_API_KEY`    | —                      | OpenRouter API key (required)                             |
| `MODEL`                  | (a free model)         | Model id, e.g. `cohere/north-mini-code:free`              |
| `MODEL_PROVIDER`         | —                      | LangChain provider, e.g. `openrouter`                     |
| `MODEL_TEMPERATURE`      | `0.8`                  | Sampling temperature for all agents                       |
| `EVAL_TIMEOUT_SECONDS`   | `300`                  | Max wait for a mentor reply / your follow-up question     |
| `MIN_TEST_CASES`         | `20`                   | Regenerate tests when a question has fewer than this      |
| `EVALUATE_BY_DEFAULT`    | `true`                 | Run the mentor unless the run params say otherwise        |
| `TRACKER_FILE`           | `tracker.json`         | Attempt/metadata store (created automatically if missing) |
| `SOLUTION_APPROACH_FILE` | `solution_approach.md` | Journal of approved solution approaches                   |
| `KB_FILE`                | `kb/coding_patterns.md`| Mentor's coding-pattern knowledge base                    |

Relative paths resolve against the repo root. `LANGSMITH_*` variables are
optional (tracing).

## Project Layout

```
main.py                     runner: fetch -> test-gen -> run -> evaluate -> track -> journal
agents/
  agent.py                  agent construction + the three public agent functions
  prompt.py                 system prompts (mentor, test generator, approach writer)
  tools.py                  agent tools (json_validator, save_in_test_file, save_learning_file)
  config.py                 Config: every .env setting in one place
utils/
  load_files.py             import solution/test modules (with force-reload for reruns)
  question_details.py       LeetCode GraphQL fetch + Playwright fallback
  readme.py                 marker-based section upsert for solution_approach.md
  logger.py                 console (INFO) + daily file (DEBUG, logs/YYYYMMDD.log)
solutions/<question_dir>/   your solution.py (+ learning.md, description.png)
testCases/<question_dir>/   generated testcase.py (a `tests` dict)
solution_approach.md        journal of approved approaches (one marked section per question)
tracker.json                per-question metadata and full attempt history
kb/coding_patterns.md       mentor's memory of your coding patterns
logs/                       daily log files
```

## Test Case Format

`testCases/<question_dir>/testcase.py` holds one dict:

```python
tests = {
    "t1": [{"nums": [2, 7, 11, 15], "target": 9}, [0, 1]],  # multi-arg: dict of kwargs
    "t2": [[1, 2, 3], 6],                                    # single arg: raw value
}
```

Each value is `[input, expected_output]`. The runner dispatches on the input's
type: a dict is unpacked as keyword arguments, anything else is passed as one
positional argument.

## Tracking

Every run appends an attempt to `tracker.json` under the question id: test
pass/fail/error counts, failed case names, time taken, outcome, the mentor's
feedback, and a timestamp. A solution that raises exceptions skips evaluation
and exits non-zero — fix the crash first, then get mentored.
