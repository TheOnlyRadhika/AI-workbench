import subprocess
from pathlib import Path
from urllib.parse import urlparse

def clone_repo(repo_url: str , workspace : str) -> str:
    parsed = urlparse(repo_url)
    if parsed.scheme not in ("http", "https") :
        raise ValueError("Invalidrepository URL")
    if parsed.netloc != "github.com":
        raise ValueError("Only github repos are supported")
    
    workspace_path = Path(workspace)
    if workspace_path.exists():
        raise FileExistsError(
            f"Workspace already exists: {workspace}"
        )
    result = subprocess.run(
        ["git", "clone", repo_url, str(workspace_path)],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Repository clone failed:\n{result.stderr}"
        )

    return str(workspace_path)