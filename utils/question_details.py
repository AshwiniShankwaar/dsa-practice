import os
import shutil
import re, html
import requests

from markdownify import markdownify as md
from playwright.sync_api import sync_playwright

from utils.logger import get_logger

logger = get_logger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GRAPHQL_URL = "https://leetcode.com/graphql"

QUESTION_QUERY = """
query questionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    title
    content
    hints
    exampleTestcaseList
    topicTags {
      name
    }
  }
}
"""


def slug_from_url(url: str) -> str:
    """Extract the problem slug from a LeetCode URL.

    Handles trailing segments too: .../problems/two-sum/description/ -> 'two-sum'.
    """
    parts = url.rstrip("/").split("/")
    return parts[parts.index("problems") + 1] if "problems" in parts else parts[-1]
def format_description(html_content: str) -> str:
    """
    Convert LeetCode HTML to clean Markdown.
    """

    text = md(
        html_content,
        heading_style="ATX",
        bullets="-"
    )
    text = html.unescape(text)
    text = text.replace("\r\n", "\n")
    text = "\n".join(line.rstrip() for line in text.splitlines())
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def format_hints(hints):
    if not hints:
        return ""
    result = ["## Hints\n"]
    for i, hint in enumerate(hints, 1):
        result.append(f"{i}. {hint}")
    return "\n".join(result)

def format_examples(examples):
    if not examples:
        return ""
    result = []
    for i, example in enumerate(examples, 1):
        lines = example.strip().split("\n")
        result.append(f"### Example {i}\n")
        result.append("```text")
        if len(lines) >= 2:
            result.append("Input:")
            result.append(lines[0])
            result.append("")
            result.append("Output:")
            result.extend(lines[1:])
        else:
            result.extend(lines)

        result.append("```")
        result.append("")

    return "\n".join(result)

def get_question_details(url: str):
    """
    Tries GraphQL first.
    If it fails, falls back to Playwright.

    Returns:
    {
        "title": str | None,       # official question title (GraphQL only)
        "type": str,               # comma-joined topic tags, e.g. "Array, Hash Table"
        "description": str,
        "examples": list,
        "hints": list,
        "screenshot": str | None
    }
    """

    slug = slug_from_url(url)

    payload = {
        "operationName": "questionDetail",
        "variables": {
            "titleSlug": slug
        },
        "query": QUESTION_QUERY
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://leetcode.com",
        "Referer": f"https://leetcode.com/problems/{slug}/",
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        logger.info("Fetching question using GraphQL...")

        response = requests.post(
            GRAPHQL_URL,
            json=payload,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise RuntimeError(data["errors"])

        question = data["data"]["question"]
        logger.info("Fetched successfully using GraphQL.")
        description = format_description(question["content"])
        examples = format_examples(
            question["exampleTestcaseList"]
        )
        hints = format_hints(
            question["hints"]
        )
        # topic tags double as the question "type" (removes the need for a type param)
        topics = ", ".join(t["name"] for t in question.get("topicTags") or [])
        return {
            "title": question.get("title"),
            "type": topics,
            "description": description,
            "examples": examples,
            "hints": hints,
            "screenshot": None
        }

    except Exception as e:

        logger.warning(
            "GraphQL failed (%s). Falling back to Playwright...",
            e
        )

        return _playwright_fallback(url)


def _playwright_fallback(url: str):
    """
    Uses Playwright to scrape the description and capture a screenshot.
    """
    screenshot_path = os.path.join(
        BASE_DIR,
        "..",
        "temp",
        "description.png"
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )
            description = page.locator(
                "[data-track-load='description_content']"
            )
            description.wait_for(
                state="visible",
                timeout=30000
            )
            description.screenshot(path=screenshot_path)
            html = description.inner_html()
            logger.info("Playwright fallback successful.")
            return {
                "title": None,   # caller falls back to a slug-derived name
                "type": "",
                "description": md(html).strip(),
                "examples": [],
                "hints": [],
                "screenshot": screenshot_path
            }
        finally:
            browser.close()

def move_file(dest,target):
    if not os.path.exists(target):
        raise ValueError("Question description is missing..")
    try:
        shutil.move(target,dest)
    except Exception as e:
        logger.info(f"Exception wile moving the file: {e}")