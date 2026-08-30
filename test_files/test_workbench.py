from unittest.mock import patch

from models import Task
from workbench import execute_github_task


def test_execute_github_task():

    task = Task(
        id="github-task",
        description="Fix the bug",
        allowed_files=["app.py"],
        forbidden_files=[],
        acceptance=["All tests pass"]
    )

    fake_result = "result"
    fake_review = "review"
    fake_handoff = "handoff"

    with patch(
        "workbench.clone_repo",
        return_value="workdir/test_repo"
    ) as mock_clone:

        with patch(
            "workbench.execute_task",
            return_value=(
                fake_result,
                fake_review,
                fake_handoff
            )
        ) as mock_execute:

            result = execute_github_task(
                task,
                "https://github.com/user/test.git",
                "workdir/test_repo"
            )

    mock_clone.assert_called_once_with(
        "https://github.com/user/test.git",
        "workdir/test_repo"
    )

    mock_execute.assert_called_once_with(
        task,
        "workdir/test_repo"
    )

    assert result == (
        fake_result,
        fake_review,
        fake_handoff
    )

def test_execute_github_task_clone_failure():
    task = Task(
        id="github-task",
        description="Fix the bug",
        allowed_files=["app.py"],
        forbidden_files=[],
        acceptance=["All tests pass"]
    )
    with patch(
        "workbench.clone_repo",
        side_effect=RuntimeError("Repository clone failed")
    ) as mock_clone:
        with patch(
            "workbench.execute_task"
        ) as mock_execute:
            try:
                execute_github_task(
                    task,
                    "https://github.com/user/test.git",
                    "workdir/test_repo"
                )
                assert False
            except RuntimeError as e:
                assert str(e) == "Repository clone failed"

    mock_clone.assert_called_once_with(
        "https://github.com/user/test.git",
        "workdir/test_repo"
    )
    mock_execute.assert_not_called()