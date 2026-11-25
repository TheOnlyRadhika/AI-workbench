import pytest

from models import Task, TaskStatus
from task_board import load_board
from task_input import create_and_register_task, create_task


def test_create_task():
    task = create_task(
        task_id="test-task",
        description="Fix the bug",
        allowed_files=["app.py"],
        acceptance=["All tests pass"],
    )

    assert isinstance(task, Task)
    assert task.id == "test-task"
    assert task.description == "Fix the bug"
    assert task.allowed_files == ["app.py"]
    assert task.acceptance == ["All tests pass"]
    assert task.forbidden_files == []


def test_task_starts_pending():
    task = create_task(
        task_id="test-task",
        description="Fix the bug",
        allowed_files=["app.py"],
        acceptance=["All tests pass"],
    )

    assert task.status == TaskStatus.PENDING


def test_empty_task_id_rejected():
    with pytest.raises(ValueError, match="Task ID cannot be empty"):
        create_task(
            task_id="",
            description="Fix the bug",
            allowed_files=["app.py"],
            acceptance=["All tests pass"],
        )


def test_empty_description_rejected():
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        create_task(
            task_id="test-task",
            description="",
            allowed_files=["app.py"],
            acceptance=["All tests pass"],
        )


def test_missing_acceptance_rejected():
    with pytest.raises(
        ValueError,
        match="At least one acceptance criterion is required",
    ):
        create_task(
            task_id="test-task",
            description="Fix the bug",
            allowed_files=["app.py"],
            acceptance=[],
        )


def test_forbidden_files():
    task = create_task(
        task_id="test-task",
        description="Fix the bug",
        allowed_files=["app.py"],
        forbidden_files=["config.py"],
        acceptance=["All tests pass"],
    )

    assert task.forbidden_files == ["config.py"]

def test_create_and_register_task(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    task = create_and_register_task(
        task_id="integration-task",
        description="Fix the bug",
        allowed_files=["app.py"],
        acceptance=["All tests pass"],
    )

    assert task.status == TaskStatus.PENDING
    board = load_board()
    task_item = next(
        item for item in board.tasks
        if item.id == "integration-task"
    )
    assert task_item.goal == "Fix the bug"
    assert task_item.status == "pending"
    assert task_item.acceptance == ["All tests pass"]