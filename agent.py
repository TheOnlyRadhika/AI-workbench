import json
from tools import TOOLS , TOOL_DEFINITIONS
from models import Task
from llm import ask_llm_with_tools , ask_llm
from tool_guard import check_tool_allowed


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

def run_agent(task):
    messages = [
        {
            "role": "system",
            "content": """
You are an AI coding agent.

Work carefully inside the repository.

Use the available tools to inspect the repository,
understand the task, make changes, and verify your work.

Do not modify files outside the allowed scope.
"""
        },
        {
            "role": "user",
            "content": task.description
        }
    ]

    while True:
        message = ask_llm_with_tools(
            messages,
            TOOL_DEFINITIONS
        )
        messages.append(message)
        if not message.tool_calls:
            return message.content
        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": str(result),
            })


def execute_tool_call(tool_call, task):
    tool_name = tool_call.function.name
    arguments = json.loads(
        tool_call.function.arguments
    )
    allowed = check_tool_allowed(
        tool_name,
        arguments,
        task.allowed_files,
        task.forbidden_files,
    )
    if not allowed:
        return (
            f"Tool call rejected: "
            f"{tool_name} is not allowed for this task."
        )
    tool = TOOLS.get(tool_name)
    if tool is None:
        return f"Unknown tool: {tool_name}"
    return tool(**arguments)