from models import RunResult

def verify_run(result: RunResult) -> RunResult:
    if result.scope_violations:
        result.actually_passing = False
        result.notes.append("Verification failed: scope violation")
        return result
    if not result.command_results:
        result.actually_passing = False
        result.notes.append("Verification failed: no commands were run")
        return result
    for command in result.command_results:
        if command["exit_code"] != 0:
            result.actually_passing = False
            result.notes.append(
                f"Verification failed: {command['command']}"
            )
            return result

    result.actually_passing = True
    result.tests_run = True

    return result