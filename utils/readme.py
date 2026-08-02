"""Deterministic per-question section management (no LLM).

Used for the solution-approach journal (main.py passes
Config.solution_approach_file as `path`). Each question's section is wrapped
in HTML comment markers so it can be found and replaced by machine:
    <!-- question:{id}:start --> ... <!-- question:{id}:end -->
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# fallback when no path is passed; the real location comes from Config
README_PATH = os.path.join(BASE_DIR, "solution_approach.md")


def _markers(question_id):
    """Return the (start, end) marker strings for a question."""
    return f"<!-- question:{question_id}:start -->", f"<!-- question:{question_id}:end -->"


def get_readme_section(question_id, path=None):
    """Return the text between this question's markers, else None."""
    path = path or README_PATH
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        content = f.read()
    start, end = _markers(question_id)
    s, e = content.find(start), content.find(end)
    if s == -1 or e == -1:
        return None
    return content[s + len(start):e].strip()


def upsert_readme_section(question_id, section_md, path=None):
    """Replace the question's existing block or append a new one.

    Creates the README if missing. UTF-8 throughout.
    """
    path = path or README_PATH
    content = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            content = f.read()
    start, end = _markers(question_id)
    block = f"{start}\n{section_md.strip()}\n{end}"
    s, e = content.find(start), content.find(end)
    if s != -1 and e != -1:
        content = content[:s] + block + content[e + len(end):]  # replace in place
    else:
        content = (content.rstrip() + "\n\n" if content.strip() else "") + block + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
