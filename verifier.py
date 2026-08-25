from models import RunResult, Task

def verify_run(result: RunResult, task: Task) -> RunResult:

    # 1. Check scope violations already detected by the tool guard
    if "No scope violations" in task.acceptance:
        if result.scope_violations:
            result.actually_passing = False
            result.notes.append(
                "Verification failed: scope violation"
            )
            return result

    # 2. Check whether tests were actually executed
    if "Tests are actually run" in task.acceptance:
        if not result.tests_run:
            result.actually_passing = False
            result.notes.append(
                "Verification failed: tests were not run"
            )
            return result

    # 3. Check whether the tests actually passed
    if "All tests pass" in task.acceptance:
        if not result.command_results:
            result.actually_passing = False
            result.notes.append(
                "Verification failed: no commands were run"
            )
            return result

        # Look at the test command result
        test_commands = [
            command
            for command in result.command_results
            if "pytest" in command["command"]
        ]

        if not test_commands:
            result.actually_passing = False
            result.notes.append(
                "Verification failed: no pytest command was run"
            )
            return result

        if test_commands[-1]["exit_code"] != 0:
            result.actually_passing = False
            result.notes.append(
                f"Verification failed: "
                f"{test_commands[-1]['command']}"
            )
            return result

    # 4. Check that the agent itself declared completion
    if "Agent reports completion" in task.acceptance:
        if not result.declared_success:
            result.actually_passing = False
            result.notes.append(
                "Verification failed: agent did not declare completion"
            )
            return result

    # Everything required by the task passed
    result.actually_passing = True
    return result