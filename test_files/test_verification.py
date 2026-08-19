from models import RunResult
from verifier import verify_run


passing_result = RunResult(
    label="passing",
    command_results=[
        {
            "command": "pytest",
            "stdout": "2 passed",
            "stderr": "",
            "exit_code": 0,
        }
    ],
)

print("Passing:", verify_run(passing_result))

failing_result = RunResult(
    label="failing",
    command_results=[
        {
            "command": "pytest",
            "stdout": "1 failed",
            "stderr": "",
            "exit_code": 1,
        }
    ],
)

print("Failing:", verify_run(failing_result))

scope_failed_result = RunResult(
    label="scope-failed",
    scope_violations=["README.md"],
    command_results=[
        {
            "command": "pytest",
            "stdout": "2 passed",
            "stderr": "",
            "exit_code": 0,
        }
    ],
)

print("Scope failed:", verify_run(scope_failed_result))