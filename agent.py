import json

from llm import ask_llm, ask_llm_with_tools
from models import CommandResult, RunResult, Task
from tool_guard import check_tool_allowed, validate_tool_arguments
from tools import TOOL_DEFINITIONS, TOOLS


def  create_agent_prompt(task:Task) -> str:
    return f"""
You are an AI coding agent working inside a software repository.
Your task is:
{task.description}

Allowed files:
{task.allowed_files}

Forbidden files:
{task.forbidden_files}

Acceptance criteria:
{task.acceptance}

Before making any changes, analyze the task and create a short plan.

Your plan should:
1. Identify which files need to be inspected.
2. Explain what changes are likely needed.
3. Explain how the changes will be verified.

Do not write code yet.
"""

def plan_task(task:Task)-> str:
    prompt = create_agent_prompt(task)
    return ask_llm(prompt)

def run_agent(task , repo_root):
    run_result = RunResult(
            label=task.description
        )


    messages = [
        {
            "role": "system",
            "content": """
            You are an AI coding agent.
            Complete the assigned coding task using the available tools.
            Rules:
            1. Inspect relevant files before modifying them.
            2. Make the smallest necessary change.
            3. Run the relevant tests after making changes.
            4. If tests fail, inspect the failure and make another correction.
            5. You may run tests multiple times.
            6. Do not declare the task complete until verification succeeds.
            7. Only use the tools explicitly provided to you. Never invent tool names
               or capabilities.
            8. If the repository already satisfies the task and the tests pass,
               do not make unnecessary changes. You may finish the task without
               modifying any files.
            """
        },
        {
            "role": "user",
            "content": task.description
        }
    ]

    max_steps = 10

    previous_tool_signature = None
    repeat_count = 0

    for step in range(max_steps):
        try:
            message = ask_llm_with_tools(
                messages,
                TOOL_DEFINITIONS
            )
        except Exception as e:
            run_result.declared_success = False
            run_result.actually_passing = False
            run_result.notes.append(f"LLM error: {e}")
            return run_result

        if message is None:
            run_result.declared_success = False
            run_result.actually_passing = False
            run_result.notes.append("LLM response was invalid or empty.")
            return run_result

        assistant_message = {
            "role": "assistant",
            "content": message.content,
        }
        if message.tool_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in message.tool_calls
            ]
        messages.append(assistant_message)

        for tool_call in (message.tool_calls or []):
            tool_signature = (
                tool_call.function.name,
                tool_call.function.arguments
            )

            if tool_signature == previous_tool_signature:
                repeat_count += 1
            else:
                repeat_count = 1

            previous_tool_signature = tool_signature

            if repeat_count >= 3:
                run_result.declared_success = False
                run_result.actually_passing = False
                run_result.notes.append(
                    "Agent stopped because it repeatedly called "
                    f"{tool_call.function.name} with the same arguments."
                )
                return run_result
            result = execute_tool_call(tool_call , task, repo_root)

            if tool_call.function.name == "run_command":
                if isinstance(result, CommandResult):
                    run_result.command_results.append({
                        "command": result.command,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "exit_code": result.exit_code
                    })
                    if "pytest" in result.command:
                        run_result.tests_run = True
                else:
                    run_result.notes.append(str(result))


            if tool_call.function.name == "write_file":
                arguments = json.loads(
                    tool_call.function.arguments
                )
                path = arguments["path"]
                if path not in run_result.files_touched:
                    run_result.files_touched.append(path)


            messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": str(result),
                        })


        if not message.tool_calls:
            run_result.declared_success = True
            run_result.notes.append(message.content)
            return run_result

    run_result.declared_success = False
    run_result.actually_passing = False
    run_result.notes.append(
        "Agent stopped because the maximum number of steps was reached."
    )

    return run_result


def execute_tool_call(tool_call, task , repo_root):
    tool_name = tool_call.function.name

    try:
        arguments = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError:
        return "Tool call rejected: invalid JSON arguments."

    print("TOOL NAME:", tool_name)
    print("ARGUMENTS:", arguments)
    allowed = check_tool_allowed(
        tool_name,
        arguments,
        task
    )

    if not allowed:
        return (
            f"Tool call rejected: "
            f"{tool_name} is not allowed for this task."
        )

     # Check whether the arguments match the tool definition
    args_valid, error = validate_tool_arguments(
        tool_name,
        arguments,
        TOOL_DEFINITIONS
    )

    if not args_valid:
        return f"Tool call rejected: {error}"


    tool = TOOLS.get(tool_name)
    if tool is None:
        return f"Unknown tool: {tool_name}"

    try:
        return tool(**arguments, repo_root=repo_root)
    except Exception as e:
        return f"Tool execution failed: {e}"
