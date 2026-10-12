import json
from pathlib import Path
from dataclasses import asdict
from models import TaskBoard, TaskItem , Task , TaskStatus

BOARD_FILE = Path("workdir") / "task_board.json"

def initialize_board():
    BOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
    if BOARD_FILE.exists():
        return
    board = TaskBoard(
        tasks=[
            TaskItem(
                id="signup-validation",
                goal="Add password validation to /signup",
                owner="builder",
                status="pending",
                acceptance=[
                    "Short passwords are rejected",
                    "Signup validation test passes"
                ],
            ),
            TaskItem(
                id="signup-tests",
                goal="Add tests for signup validation",
                owner="builder",
                status="pending",
                acceptance=[
                    "Validation behavior is covered by tests"
                ],
            ),
        ]
    )

    with BOARD_FILE.open("w") as file:
        json.dump(asdict(board), file, indent=4)



def load_board():
    with BOARD_FILE.open("r") as file:
        data = json.load(file)
    tasks = [
        TaskItem(**task)
        for task in data["tasks"]
    ]
    return TaskBoard(tasks=tasks)


def save_board(board: TaskBoard):
    with BOARD_FILE.open("w") as file:
        json.dump(asdict(board), file, indent=4)

def get_next_task(board: TaskBoard) -> TaskItem | None:
    for task in board.tasks:
        if task.status == TaskStatus.PENDING.value:
            return task
    return None

def complete_task(board: TaskBoard, task_id: str)-> bool:# find the task and mark it as done
    for task in board.tasks:
        if task.id == task_id:
            task.status = TaskStatus.COMPLETED.value
            return True

    return False


def mark_task_in_progress(board: TaskBoard, task_id: str) -> bool:
    for task in board.tasks:
        if task.id == task_id:
            task.status = TaskStatus.RUNNING.value
            return True

    return False

def add_task(board: TaskBoard, task: Task) -> TaskItem:
    """Add a Task to the task board."""

    for existing_task in board.tasks:
        if existing_task.id == task.id:
            raise ValueError(f"Task already exists: {task.id}")

    task_item = TaskItem(
        id=task.id,
        goal=task.description,
        owner="agent",
        status=task.status.value,
        acceptance=task.acceptance,
    )

    board.tasks.append(task_item)
    return task_item

def update_task_status(board: TaskBoard, task_id: str, status: str) -> bool:
    """Update the status of a task on the task board."""

    for task in board.tasks:
        if task.id == task_id:
            task.status = status
            return True
    return False