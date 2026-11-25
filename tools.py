from collections.abc import Callable
from pathlib import Path
from typing import Any

from feedback import run_command


def list_files(repo_root) -> list[str]:
    root_path = Path(repo_root)
    if not root_path.exists():
        raise FileNotFoundError(f"Directory not found: {repo_root}")
    ignored = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        "agentic-ai",
    }
    files = []

    for path in root_path.rglob("*.py"):
        if not path.is_file():
            continue
        if any(part in ignored for part in path.parts):
            continue
        files.append(str(path.relative_to(root_path)))
    return files


def read_file(path : str , repo_root : str) -> str:
    file_path = Path(repo_root)/path
    if not file_path.exists():
        raise FileNotFoundError(f"file not found: {path}")
    return file_path.read_text()

def write_file(path: str, content: str , repo_root:str) -> str:
    file_path = Path(repo_root)/path

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)

    return f"Successfully wrote {path}"


TOOLS: dict[str, Callable[..., Any]] = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files inside the repository.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to read."
                    }
                },
                "required": ["path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to write."
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file."
                    }
                },
                "required": ["path", "content"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a command in the repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Command to execute."
                    }
                },
                "required": ["command"]
            }
        }
    }
]