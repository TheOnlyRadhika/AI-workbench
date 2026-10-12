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

def validate_tool_arguments(tool_name, arguments, tool_definitions):
    for tool in tool_definitions:
        function = tool["function"]

        if function["name"] == tool_name:
            allowed_arguments = set(
                function["parameters"]["properties"].keys()
            )
            unexpected_arguments = (
                set(arguments.keys()) - allowed_arguments
            )
            if unexpected_arguments:
                return False, (
                    f"Unexpected arguments for {tool_name}: "
                    f"{unexpected_arguments}"
                )
            return True, ""

    return False, f"Unknown tool: {tool_name}"