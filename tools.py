from pathlib import Path
from feedback import run_command

from pathlib import Path


def list_files(root: str = ".") -> list[str]:
    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(f"Directory not found: {root}")
    return [
        str(path)
        for path in root_path.rglob("*")
        if path.is_file()
    ]


def read_file(path : str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return FileNotFoundError(f"file not found: {path}")
    return file_path.read_text()

def write_file(path: str, content: str) -> str:
    file_path = Path(path)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)

    return f"Successfully wrote {path}"


TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
}

TOOL_DEFINITIONS = [
    {
        "name": "list_files",
        "description": "List files inside the repository.",
        "parameters": {
            "type": "object",
            "properties": {
                "root": {
                    "type": "string",
                    "description": "Directory to search from."
                }
            },
            "required": []
        }
    },
    {
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
    },
    {
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
                    "description": "Complete new contents of the file."
                }
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "run_command",
        "description": "Run a shell command in the repository.",
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
    },
]