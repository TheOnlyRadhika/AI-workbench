from models import Task, RunResult
from verifier import verify_run


def make_task():
    return Task(
        description="Test verification",
        allowed_files=["app.py"],
        forbidden_files=[],
        acceptance=[
            "All tests pass",
            "Tests are actually run",
            "No scope violations",
            "Agent reports completion"
        ]
    )


def test_tests_not_run():
    task = make_task()

    result = RunResult(
        label="test",
        tests_run=False,
        declared_success=True
    )

    result = verify_run(result, task)

    assert result.actually_passing is False
    assert "tests were not run" in result.notes[0]


def test_tests_failed():
    task = make_task()

    result = RunResult(
        label="test",
        tests_run=True,
        declared_success=True,
        command_results=[
            {
                "command": "pytest -q",
                "stdout": "",
                "stderr": "1 failed",
                "exit_code": 1
            }
        ]
    )

    result = verify_run(result, task)

    assert result.actually_passing is False


def test_scope_violation():
    task = make_task()

    result = RunResult(
        label="test",
        tests_run=True,
        declared_success=True,
        scope_violations=["README.md"],
        command_results=[
            {
                "command": "pytest -q",
                "stdout": "1 passed",
                "stderr": "",
                "exit_code": 0
            }
        ]
    )

    result = verify_run(result, task)

    assert result.actually_passing is False


def test_agent_did_not_declare_completion():
    task = make_task()

    result = RunResult(
        label="test",
        tests_run=True,
        declared_success=False,
        command_results=[
            {
                "command": "pytest -q",
                "stdout": "1 passed",
                "stderr": "",
                "exit_code": 0
            }
        ]
    )

    result = verify_run(result, task)

    assert result.actually_passing is False


def test_successful_verification():
    task = make_task()

    result = RunResult(
        label="test",
        tests_run=True,
        declared_success=True,
        scope_violations=[],
        command_results=[
            {
                "command": "pytest -q",
                "stdout": "1 passed",
                "stderr": "",
                "exit_code": 0
            }
        ]
    )

    result = verify_run(result, task)

    assert result.actually_passing is True