"""Commit and push a solved question's files.

Plain git via subprocess — no LLM agent, the steps are deterministic.
On a rejected push the commit is soft-reset (changes stay staged) and the
user is asked to merge manually.
"""
import subprocess

from utils.logger import get_logger

logger = get_logger(__name__)


def _git(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def commit_and_push(repo_root, question_dir, question_name, readme_path):
    """git add solution + test cases + approach readme, commit, push.

    If the push is rejected (remote diverged / merge conflict), the commit is
    undone with `git reset --soft HEAD~1` so no changes are lost, and a
    warning asks the user to pull/merge themselves.
    """
    paths = [f"solutions/{question_dir}", f"testCases/{question_dir}", readme_path]
    add = _git("add", "--", *paths, cwd=repo_root)
    if add.returncode != 0:
        logger.warning("git add failed:\n%s", add.stderr or add.stdout)
        return

    if _git("diff", "--cached", "--quiet", cwd=repo_root).returncode == 0:
        logger.info("Nothing new to commit for question %s", question_name)
        return

    msg = f"committing the solution of question {question_name}"
    commit = _git("commit", "-m", msg, cwd=repo_root)
    if commit.returncode != 0:
        logger.warning("git commit failed:\n%s", commit.stderr or commit.stdout)
        return

    push = _git("push", cwd=repo_root)
    if push.returncode == 0:
        logger.info("Pushed: %s", msg)
        return

    # push rejected: undo the commit, keep every change staged for the user
    _git("reset", "--soft", "HEAD~1", cwd=repo_root)
    logger.warning(
        "git push failed — the commit was soft-reset, all your changes are "
        "still staged. Please take a look, pull/merge manually and commit "
        "yourself.\n%s",
        push.stderr or push.stdout,
    )


if __name__ == "__main__":
    # self-check: real temp repos exercise the success and rejected-push paths
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        remote = os.path.join(tmp, "remote.git")
        subprocess.run(["git", "init", "--bare", remote], check=True, capture_output=True)

        def clone(name):
            path = os.path.join(tmp, name)
            subprocess.run(["git", "clone", remote, path], check=True, capture_output=True)
            _git("config", "user.email", "t@t", cwd=path)
            _git("config", "user.name", "t", cwd=path)
            return path

        repo = clone("repo")
        open(os.path.join(repo, "seed.txt"), "w").write("seed\n")
        _git("add", ".", cwd=repo)
        _git("commit", "-m", "seed", cwd=repo)
        assert _git("push", "-u", "origin", "HEAD", cwd=repo).returncode == 0

        # success path
        os.makedirs(os.path.join(repo, "solutions/two_sum"))
        os.makedirs(os.path.join(repo, "testCases/two_sum"))
        open(os.path.join(repo, "solutions/two_sum/solution.py"), "w").write("x = 1\n")
        open(os.path.join(repo, "testCases/two_sum/testcase.py"), "w").write("t = 1\n")
        open(os.path.join(repo, "readme.md"), "w").write("# approach\n")
        commit_and_push(repo, "two_sum", "Two Sum", "readme.md")
        log = _git("log", "--oneline", "origin/master..HEAD", cwd=repo)
        assert log.stdout.strip() == "" or "master" not in log.stderr, "push failed"

        # rejected-push path: another clone pushes first, so ours is rejected
        other = clone("other")
        open(os.path.join(other, "seed.txt"), "a").write("diverge\n")
        _git("add", ".", cwd=other)
        _git("commit", "-m", "diverge", cwd=other)
        assert _git("push", cwd=other).returncode == 0

        head_before = _git("rev-parse", "HEAD", cwd=repo).stdout.strip()
        open(os.path.join(repo, "solutions/two_sum/solution.py"), "w").write("x = 2\n")
        commit_and_push(repo, "two_sum", "Two Sum", "readme.md")
        # commit must be soft-reset: HEAD unchanged, edit still staged
        assert _git("rev-parse", "HEAD", cwd=repo).stdout.strip() == head_before
        assert _git("diff", "--cached", "--quiet", cwd=repo).returncode == 1

    print("git_publish self-check passed")
