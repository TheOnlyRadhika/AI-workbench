from unittest.mock import patch

from models import Task
from agent import run_agent


def test_repeated_tool_call_stops_agent():

    task = Task(
        id="convergence-test",
        description="Test repeated tool calls",
        allowed_files=["app.py"],
        forbidden_files=[],
        acceptance=[]
    )

    # Fake tool call
    class FakeFunction:
        name = "list_files"
        arguments = "{}"

    class FakeToolCall:
        id = "test-call"
        function = FakeFunction()

    class FakeMessage:
        content = ""
        tool_calls = [FakeToolCall()]

    with patch(
        "agent.ask_llm_with_tools",
        return_value=FakeMessage()
    ):

        result = run_agent(
            task,
            "workdir/demo_repo"
        )

    assert result.declared_success is False
    assert result.actually_passing is False

    assert any(
        "repeatedly called list_files" in note
        for note in result.notes
    )