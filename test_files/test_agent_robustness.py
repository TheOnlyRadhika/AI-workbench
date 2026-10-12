from unittest.mock import Mock
from agent import execute_tool_call , run_agent


def test_execute_tool_call_handles_invalid_json():
    tool_call = Mock()
    tool_call.function.name = "read_file"
    tool_call.function.arguments = '{"path": "models.py"'

    result = execute_tool_call(
        tool_call,
        task=Mock(),
        repo_root="."
    )

    assert result == "Tool call rejected: invalid JSON arguments."



def test_execute_tool_call_handles_tool_exception():
    tool_call = Mock()
    tool_call.function.name = "read_file"
    tool_call.function.arguments = '{"path": "models.py"}'

    fake_task = Mock()
    fake_task.allowed_files = ["does_not_exist.py"]
    fake_task.forbidden_files = []

    # We need the actual tool to fail.
    # Use a path that does not exist.
    tool_call.function.arguments = '{"path": "does_not_exist.py"}'

    result = execute_tool_call(
        tool_call,
        task=fake_task,
        repo_root="."
    )
    assert result.startswith("Tool execution failed:")



def test_run_agent_handles_non_command_result(monkeypatch):
    task = Mock()
    task.description = "Test task"
    task.allowed_files = []
    task.forbidden_files = []
    task.acceptance = []

    # Fake LLM response: it asks to run a command
    tool_call = Mock()
    tool_call.id = "test-tool-call"
    tool_call.function.name = "run_command"
    tool_call.function.arguments = '{"command": "pytest"}'

    llm_message = Mock()
    llm_message.content = ""
    llm_message.tool_calls = [tool_call]

    # First LLM response asks for the tool.
    # Second response has no tool calls, so the agent finishes.
    responses = iter([
        llm_message,
        Mock(content="Finished", tool_calls=[]),
    ])

    monkeypatch.setattr(
        "agent.ask_llm_with_tools",
        lambda messages, tools: next(responses)
    )

    # Simulate a rejected/failed tool call.
    monkeypatch.setattr(
        "agent.execute_tool_call",
        lambda tool_call, task, repo_root:
            "Tool call rejected: command is not allowed."
    )

    result = run_agent(task, ".")

    assert "Tool call rejected: command is not allowed." in result.notes
    assert result.tests_run is False



def test_run_agent_handles_llm_failure(monkeypatch):
    task = Mock()
    task.description = "Test task"
    task.allowed_files = []
    task.forbidden_files = []
    task.acceptance = []

    def fake_llm_call(messages, tools):
        raise RuntimeError("Groq API failed")

    monkeypatch.setattr(
        "agent.ask_llm_with_tools",
        fake_llm_call
    )
    result = run_agent(task, ".")

    assert result.declared_success is False
    assert result.actually_passing is False
    assert "LLM error: Groq API failed" in result.notes



def test_run_agent_handles_unexpected_llm_response(monkeypatch):
    task = Mock()
    task.description = "Test task"
    task.allowed_files = []
    task.forbidden_files = []
    task.acceptance = []

    # Simulate a successful API call that returns an invalid response.
    monkeypatch.setattr(
        "agent.ask_llm_with_tools",
        lambda messages, tools: None
    )

    result = run_agent(task, ".")

    assert result.declared_success is False
    assert result.actually_passing is False
    assert any(
        "LLM response" in note
        for note in result.notes
    )