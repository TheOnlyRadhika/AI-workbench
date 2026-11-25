from models import Task
from task_board import add_task, initialize_board, load_board, save_board


def create_task(
    task_id: str,
    description: str,
    allowed_files: list[str],
    acceptance: list[str],
    forbidden_files: list[str] | None = None,
) -> Task:

    if not task_id.strip():
        raise ValueError("Task ID cannot be empty")

    if not description.strip():
        raise ValueError("Task description cannot be empty")

    if not acceptance:
        raise ValueError("At least one acceptance criterion is required")

    return Task(
        id=task_id,
        description=description,
        allowed_files=allowed_files,
        forbidden_files=forbidden_files or [],
        acceptance=acceptance,
    )




def create_and_register_task(
    task_id: str,
    description: str,
    allowed_files: list[str],
    acceptance: list[str],
    forbidden_files: list[str] | None = None,
) -> Task:

    task = create_task(
        task_id=task_id,
        description=description,
        allowed_files=allowed_files,
        acceptance=acceptance,
        forbidden_files=forbidden_files,
    )
    initialize_board()
    board = load_board()
    add_task(board, task)
    save_board(board)

    return task