"""Central logging setup: importing this module configures logging once.

Everything goes to a daily log file (logs/YYYYMMDD.log at the project root,
DEBUG and up) and to the console (INFO and up).
"""
import logging, sys
import os
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
LOG_DIR = os.path.join(BASE_PATH, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # FileHandler won't create the dir itself

_file_handler = logging.FileHandler(
    filename=os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y%m%d')}.log"),
    encoding="utf-8",
)
_file_handler.setLevel(logging.DEBUG)

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.INFO)  # keep the terminal readable; file gets DEBUG

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[_file_handler, _console_handler],  # basicConfig needs a LIST
)

# keep noisy third-party HTTP clients (used by the agents) at WARNING+
for _noisy in ("httpx", "httpcore", "urllib3", "asyncio","langsmith"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)


def get_logger(name):
    """Return a named logger (pass __name__)."""
    return logging.getLogger(name)
