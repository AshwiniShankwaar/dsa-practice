# Tools given to the agents: JSON validation, test-file persistence, learning notes.
import json
import os

from langchain.tools import tool

from utils.load_files import _load_testCase
from utils.logger import get_logger

logger = get_logger(__name__)


@tool
def json_validator(content: str | dict):
    """Validate a JSON string (or pass through a dict) and return the parsed dict.

    Returns an "INVALID JSON: ..." error string on parse failure so the agent
    can correct its output and retry within the same run.
    """
    if not content or len(content) == 0:
        return {}
    if isinstance(content, dict):
        return content
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        # Let the one-shot agent self-correct instead of crashing the run.
        return f"INVALID JSON: {e}"


@tool
def save_in_test_file(test_cases: dict, test_cases_path):
    """Merge test_cases into <test_cases_path>/testcase.py and save it.

    test_cases_path is testCases/<question_dir>/ (the dir is the question's
    slug with '-' -> '_'). The file is a Python module holding a single
    `tests` dict. Existing tests are kept; new keys are added/overwritten.
    Returns a status message.
    """
    # the question dir doubles as the module name for reloading existing tests
    question_dir = os.path.basename(os.path.normpath(test_cases_path))
    try:
        # Existing tests, if any — defensive in case the loader raises.
        try:
            existing = _load_testCase(question_dir)
        except (ModuleNotFoundError, AttributeError):
            existing = {}
        # Copy: the loaded module attribute is cached by importlib.
        merged = dict(existing) if isinstance(existing, dict) else {}
        for key, value in test_cases.items():
            merged[key] = value

        test_case_file = os.path.join(test_cases_path, "testcase.py")
        os.makedirs(test_cases_path, exist_ok=True)
        # repr of a JSON-compatible dict is valid Python source.
        with open(test_case_file, "w", encoding="utf-8") as f:
            f.write(f"tests = {merged!r}\n")
        return f"Saved {len(merged)} test cases to {test_case_file}"
    except Exception as e:
        logger.warning("Error while saving testcases for %s: %s", question_dir, e)
        return f"ERROR saving test cases: {e}"


@tool
def save_learning_file(content: str, file_path: str) -> str:
    """Write (or overwrite) a markdown learning file at file_path."""
    try:
        parent = os.path.dirname(file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Learning file saved at {file_path}"
    except Exception as e:
        logger.warning("Error while saving learning file %s: %s", file_path, e)
        return f"ERROR saving learning file: {e}"
