
from pathlib import Path

from github import clone_repo
from initializer import initialize_workbench
from orchestrator import execute_task
from task_input import create_and_register_task


def run_workbench(
    repo_url: str,
    workspace: str,
    task_id: str,
    description: str,
    allowed_files: list[str],
    acceptance: list[str],
    forbidden_files: list[str] | None = None,
):
    """Initialize the workbench and execute a repository-level coding task."""
    # 1. Initialize persistent workbench state and task board.
    initialize_workbench()
    # 2. Validate, create, and register the task.
    task = create_and_register_task(
        task_id=task_id,
        description=description,
        allowed_files=allowed_files,
        acceptance=acceptance,
        forbidden_files=forbidden_files,
    )
    # 3. Prepare the workspace and clone the repository.
    workspace_path = Path(workspace)
    workspace_path.parent.mkdir(parents=True, exist_ok=True)

    repo_root = clone_repo(
        repo_url,
        str(workspace_path),
    )
    # 4. Execute the existing orchestration pipeline.
    return execute_task(task, repo_root)



def execute_github_task(task, repo_url: str, workspace: str):
    """Execute an already-created task against a GitHub repository."""

    repo_root = clone_repo(repo_url, workspace)
    return execute_task(task, repo_root)
