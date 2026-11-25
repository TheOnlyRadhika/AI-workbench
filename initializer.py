from pathlib import Path

from state import initialize_state
from task_board import initialize_board

ROOT = Path(__file__).parent
INSTRUCTIONS_FILE = ROOT / "AGENTS.md"


def check_instructions() -> None:
    if not INSTRUCTIONS_FILE.exists():
        raise FileNotFoundError("AGENTS.md is missing")

def initialize_workbench():
    check_instructions()
    initialize_state()
    initialize_board()
