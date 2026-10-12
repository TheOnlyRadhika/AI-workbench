from task_board import initialize_board, load_board, save_board , get_next_task
import pytest
from models import Task, TaskBoard, TaskItem , TaskStatus
from task_board import add_task , update_task_status


initialize_board()

board = load_board()

print("Initial board:")
for task in board.tasks:
    print(task)

board.tasks[0].status = "in_progress"

save_board(board)

updated_board = load_board()

print("\nUpdated board:")
for task in updated_board.tasks:
    print(task)

next_task = get_next_task(board)
print("\nNext Task:")
print(next_task)

def test_add_duplicate_task_rejected():
    board = TaskBoard()

    task = Task(
        id="test-task",
        description="Fix the bug",
        allowed_files=["app.py"],
        forbidden_files=[],
        acceptance=["All tests pass"],
    )

    add_task(board, task)

    with pytest.raises(ValueError, match="Task already exists: test-task"):
        add_task(board, task)

def test_update_task_status():
    board = TaskBoard(
        tasks=[
            TaskItem(
                id="test-task",
                goal="Fix the bug",
                owner="agent",
                status="pending",
                acceptance=["Tests pass"],
            )
        ]
    )
    updated = update_task_status(
        board,
        "test-task",
        "running",
    )
    assert updated is True
    assert board.tasks[0].status == "running"



def test_update_missing_task_status():
    board = TaskBoard()
    updated = update_task_status(
        board,
        "does-not-exist",
        "running",
    )
    assert updated is False