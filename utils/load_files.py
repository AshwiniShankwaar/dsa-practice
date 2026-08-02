import importlib


def _load_solution(question_dir, force_reload=False):
    """Import solutions/<question_dir>/solution.py and return an instance of its
    Solution class. question_dir is the leetcode slug with '-' -> '_'
    (e.g. "two_sum").

    Pass force_reload=True to pick up edits made to solution.py during this
    process (e.g. the evaluation agent's rerun_solution tool).
    Raises ModuleNotFoundError if the solution file is missing (a real error).
    """
    if force_reload:
        importlib.invalidate_caches()
    solution_module = importlib.import_module(f"solutions.{question_dir}.solution")
    if force_reload:
        solution_module = importlib.reload(solution_module)
    SolutionClass = getattr(solution_module, "Solution")  # Solution class inside solution.py
    return SolutionClass()


def _load_testCase(question_dir, force_reload=False):
    """Return the `tests` dict from testCases/<question_dir>/testcase.py, or {}
    if the file doesn't exist yet (main uses the count to decide whether to
    generate).

    Pass force_reload=True after the agent writes the file mid-run so the
    fresh module is picked up instead of a cached (or negative) import.
    """
    module_name = f"testCases.{question_dir}.testcase"
    try:
        if force_reload:
            importlib.invalidate_caches()  # file was written during this process
        testcase_module = importlib.import_module(module_name)
        if force_reload:
            testcase_module = importlib.reload(testcase_module)
        return getattr(testcase_module, "tests")  # tests dict
    except ModuleNotFoundError:
        return {}  # no test file yet -> caller will generate one
