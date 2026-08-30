from github import clone_repo

repo_url = "https://github.com/pytest-dev/pytest.git"
workspace = "workdir/real_repo"

repo_root = clone_repo(repo_url, workspace)

print("Cloned repository:", repo_root)