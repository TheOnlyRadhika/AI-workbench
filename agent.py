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

def run_agent(task , repo_root):
    messages = [
        {
            "role": "system",
            "content": """
            You are an AI coding agent.
            Work carefully inside the repository.
            Use the available tools to inspect the repository,understand the task, 
                make changes, and verify your work.
            Do not modify files outside the allowed scope.
            """
        },
        {
            "role": "user",
            "content": task.description
        }
    ]

    max_steps = 10
    for step in range(max_steps):
        message = ask_llm_with_tools(
            messages,
            TOOL_DEFINITIONS
        )
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
        if not message.tool_calls:
            return message.content
        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call , task, repo_root)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": str(result),
            })
        
    return "Agent stopped because the maximum number of steps was reached."


def execute_tool_call(tool_call, task , repo_root):
    tool_name = tool_call.function.name
    arguments = json.loads(
        tool_call.function.arguments
    )
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
    tool = TOOLS.get(tool_name)
    if tool is None:
        return f"Unknown tool: {tool_name}"
    return tool(
            **arguments,
            repo_root= repo_root
            )