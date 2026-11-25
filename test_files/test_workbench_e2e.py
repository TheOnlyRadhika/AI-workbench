
import pytest

from models import RunResult, TaskStatus
from state import load_state
from task_board import load_board
from workbench import run_workbench


def test_workbench_end_to_end_approved_task(monkeypatch, tmp_path):
    # Keep test data separate from the real workbench files.
    monkeypatch.chdir(tmp_path)

    repo_root = tmp_path / "workspace" / "repo"
    repo_root.mkdir(parents=True)

    # Simulate repository cloning without contacting GitHub.
    monkeypatch.setattr(
        "workbench.clone_repo",
        lambda repo_url, workspace: str(repo_root),
    )

    # Skip the AGENTS.md check for this isolated test.
    monkeypatch.setattr(
        "workbench.initialize_workbench",
        lambda: None,
    )

    # Simulate an agent that successfully completes the task.
    def fake_run_agent(task, repo_root):
        return RunResult(
            label="Task execution completed",
            declared_success=True,
            actually_passing=True,
            tests_run=True,
            files_touched=["app.py"],
            notes=["Input validation added."],
        )

    monkeypatch.setattr("orchestrator.run_agent", fake_run_agent)

    result, review, handoff = run_workbench(
        repo_url="https://github.com/example/repo.git",
        workspace=str(tmp_path / "workspace" / "repo"),
        task_id="e2e-task-1",
        description="Add input validation",
        allowed_files=["app.py"],
        acceptance=["Invalid input is rejected"],
    )

    # The agent's result should reach the reviewer successfully.
    assert result.actually_passing is True
    assert review.approved is True

    # A handoff should be generated.
    assert handoff is not None
    assert handoff.task_id == "e2e-task-1"

    # The task should be persisted as completed.
    from task_board import load_board

    board = load_board()
    task = next(
        item for item in board.tasks
        if item.id == "e2e-task-1"
    )
    assert task.status == "completed"



def test_workbench_end_to_end_rejected_task(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    repo_root = tmp_path / "workspace" / "repo"
    repo_root.mkdir(parents=True)

    monkeypatch.setattr(
        "workbench.clone_repo",
        lambda repo_url, workspace: str(repo_root),
    )

    monkeypatch.setattr(
        "workbench.initialize_workbench",
        lambda: None,
    )

    # Simulate an agent whose verification has failed.
    def fake_run_agent(task, repo_root):
        return RunResult(
            label="Task execution failed",
            declared_success=True,
            actually_passing=False,
            tests_run=False,
            files_touched=["app.py"],
            notes=["The required checks did not pass."],
        )

    monkeypatch.setattr("orchestrator.run_agent", fake_run_agent)

    result, review, handoff = run_workbench(
        repo_url="https://github.com/example/repo.git",
        workspace=str(tmp_path / "workspace" / "repo"),
        task_id="e2e-task-2",
        description="Add input validation",
        allowed_files=["app.py"],
        acceptance=["All tests pass"],
    )

    # The reviewer should reject the task.
    assert result.actually_passing is False
    assert review.approved is False
    assert "Verification did not pass" in review.issues

    # A handoff should still be generated.
    assert handoff is not None
    assert handoff.task_id == "e2e-task-2"

    # The failed status should persist on disk.
    from task_board import load_board

    board = load_board()
    task = next(
        item for item in board.tasks
        if item.id == "e2e-task-2"
    )
    assert task.status == "failed"



def test_workbench_agent_exception_marks_task_failed(
    monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)

    repo_root = tmp_path / "workspace" / "repo"
    repo_root.mkdir(parents=True)

    monkeypatch.setattr(
        "workbench.clone_repo",
        lambda repo_url, workspace: str(repo_root),
    )

    monkeypatch.setattr(
        "workbench.initialize_workbench",
        lambda: None,
    )

    def fake_run_agent(task, repo_root):
        raise RuntimeError("Simulated agent failure")

    monkeypatch.setattr("orchestrator.run_agent", fake_run_agent)

    with pytest.raises(RuntimeError, match="Simulated agent failure"):
        run_workbench(
            repo_url="https://github.com/example/repo.git",
            workspace=str(tmp_path / "workspace" / "repo"),
            task_id="e2e-task-failure",
            description="Add input validation",
            allowed_files=["app.py"],
            acceptance=["All tests pass"],
        )

    board = load_board()
    task = next(
        item for item in board.tasks
        if item.id == "e2e-task-failure"
    )

    assert task.status == TaskStatus.FAILED.value

    state = load_state()
    assert "Simulated agent failure" in state.blockers




def test_workbench_verifier_exception_marks_task_failed(
    monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)
    repo_root = tmp_path / "workspace" / "repo"
    repo_root.mkdir(parents=True)
    monkeypatch.setattr(
        "workbench.clone_repo",
        lambda repo_url, workspace: str(repo_root),
    )
    monkeypatch.setattr(
        "workbench.initialize_workbench",
        lambda: None,
    )
    def fake_run_agent(task, repo_root):
        return RunResult(
            label="Agent finished",
            declared_success=True,
            actually_passing=True,
            tests_run=True,
            files_touched=["app.py"],
        )

    def fake_verify_run(result, task):
        raise RuntimeError("Simulated verifier failure")

    monkeypatch.setattr("orchestrator.run_agent", fake_run_agent)
    monkeypatch.setattr("orchestrator.verify_run", fake_verify_run)

    with pytest.raises(RuntimeError, match="Simulated verifier failure"):
        run_workbench(
            repo_url="https://github.com/example/repo.git",
            workspace=str(tmp_path / "workspace" / "repo"),
            task_id="e2e-verifier-failure",
            description="Add input validation",
            allowed_files=["app.py"],
            acceptance=["All tests pass"],
        )

    from models import TaskStatus
    from state import load_state
    from task_board import load_board

    board = load_board()
    task = next(
        item for item in board.tasks
        if item.id == "e2e-verifier-failure"
    )
    assert task.status == TaskStatus.FAILED.value
    state = load_state()
    assert "Simulated verifier failure" in state.blockers


def test_workbench_reviewer_exception_marks_task_failed(
    monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)

    repo_root = tmp_path / "workspace" / "repo"
    repo_root.mkdir(parents=True)

    monkeypatch.setattr(
        "workbench.clone_repo",
        lambda repo_url, workspace: str(repo_root),
    )
    monkeypatch.setattr(
        "workbench.initialize_workbench",
        lambda: None,
    )

    def fake_run_agent(task, repo_root):
        return RunResult(
            label="Agent finished",
            declared_success=True,
            actually_passing=True,
            tests_run=True,
            files_touched=["app.py"],
        )

    def fake_review_run(task, result):
        raise RuntimeError("Simulated reviewer failure")

    monkeypatch.setattr("orchestrator.run_agent", fake_run_agent)
    monkeypatch.setattr("orchestrator.review_run", fake_review_run)

    with pytest.raises(
        RuntimeError, match="Simulated reviewer failure"
    ):
        run_workbench(
            repo_url="https://github.com/example/repo.git",
            workspace=str(tmp_path / "workspace" / "repo"),
            task_id="e2e-reviewer-failure",
            description="Add input validation",
            allowed_files=["app.py"],
            acceptance=["All tests pass"],
        )

    board = load_board()
    task = next(
        item for item in board.tasks
        if item.id == "e2e-reviewer-failure"
    )

    assert task.status == TaskStatus.FAILED.value

    state = load_state()
    assert "Simulated reviewer failure" in state.blockers


def test_workbench_handoff_exception_is_recorded(
    monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)

    repo_root = tmp_path / "workspace" / "repo"
    repo_root.mkdir(parents=True)

    monkeypatch.setattr(
        "workbench.clone_repo",
        lambda repo_url, workspace: str(repo_root),
    )
    monkeypatch.setattr(
        "workbench.initialize_workbench",
        lambda: None,
    )

    def fake_run_agent(task, repo_root):
        return RunResult(
            label="Agent finished",
            declared_success=True,
            actually_passing=True,
            tests_run=True,
            files_touched=["app.py"],
        )

    def fake_create_handoff(state, task, summary):
        raise RuntimeError("Simulated handoff failure")

    monkeypatch.setattr("orchestrator.run_agent", fake_run_agent)
    monkeypatch.setattr("orchestrator.create_handoff", fake_create_handoff)

    result, review, handoff = run_workbench(
        repo_url="https://github.com/example/repo.git",
        workspace=str(tmp_path / "workspace" / "repo"),
        task_id="e2e-handoff-failure",
        description="Add input validation",
        allowed_files=["app.py"],
        acceptance=["Invalid input is rejected"],
    )

    assert review.approved is True
    assert result.actually_passing is True
    assert handoff is None

    board = load_board()
    task = next(
        item for item in board.tasks
        if item.id == "e2e-handoff-failure"
    )
    assert task.status == TaskStatus.COMPLETED.value

    state = load_state()
    assert any(
        "Simulated handoff failure" in blocker
        for blocker in state.blockers
    )
