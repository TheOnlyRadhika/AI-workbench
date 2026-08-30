from github import clone_repo
from orchestrator import execute_task


def execute_github_task(task, repo_url, workspace):

    repo_root = clone_repo(
        repo_url,
        workspace
    )

    return execute_task(
        task,
        repo_root
    )