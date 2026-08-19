from pathlib import Path


def check_path_allowed(path: str, allowed_files: list[str], forbidden_files: list[str]) -> bool:
    normalized = Path(path)
    if str(normalized) in forbidden_files:
        return False
    if str(normalized) not in allowed_files:
        return False
    return True

def check_tool_allowed(tool_name: str, arguments: dict, task: object) -> bool:
    if tool_name == "read_file":
        return check_path_allowed(
            arguments["path"],
            task.allowed_files,
            task.forbidden_files
        )
    if tool_name == "write_file":
        return check_path_allowed(
            arguments["path"],
            task.allowed_files,
            task.forbidden_files
        )
    if tool_name == "list_files":
        return True
    if tool_name == "run_command":
        return check_command_allowed(
            arguments["command"]
        )
    return False


ALLOWED_COMMANDS = [
    "pytest",
    "python",
    "python3",
]


def check_command_allowed(command):
    parts = command.strip().split()
    if not parts:
        return False
    first_word = parts[0]
    return first_word in ALLOWED_COMMANDS