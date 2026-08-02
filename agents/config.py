import os
from pathlib import Path
from dotenv import load_dotenv

BASH_PATH = Path(__file__).resolve().parents[1]
load_dotenv(os.path.join(BASH_PATH, ".env"))


def _path(value: str) -> str:
    """Resolve a path from .env against the repo root (absolute paths pass through)."""
    return os.path.join(BASH_PATH, value)


def _bool(value: str) -> bool:
    return value.strip().lower() in ("1", "true", "yes", "on")


class Config:
    """All tunable settings, loaded from the repo-root .env with safe defaults."""
    # --- model (OpenRouter by default) ---
    model = os.getenv("MODEL", default="nvidia/nemotron-3-ultra-550b-a55b:free")
    model_api_key = os.getenv("OPEN_ROUTER_API_KEY")
    model_provider = os.getenv("MODEL_PROVIDER")
    model_temperature = float(os.getenv("MODEL_TEMPERATURE", "0.8"))

    # --- behaviour knobs ---
    # max seconds to wait on the evaluation agent / a follow-up question
    eval_timeout_seconds = int(os.getenv("EVAL_TIMEOUT_SECONDS", "300"))
    # regenerate test cases when fewer than this many exist
    min_test_cases = int(os.getenv("MIN_TEST_CASES", "20"))
    # global default for running the mentor agent ("evaluate" in the CLI params overrides)
    evaluate_by_default = _bool(os.getenv("EVALUATE_BY_DEFAULT", "true"))

    # --- file locations (relative paths resolve against the repo root) ---
    tracker_file = _path(os.getenv("TRACKER_FILE", "tracker.json"))
    solution_approach_file = _path(os.getenv("SOLUTION_APPROACH_FILE", "solution_approach.md"))
    kb_file = _path(os.getenv("KB_FILE", "kb/coding_patterns.md"))
