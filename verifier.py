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
    
    last_command = result.command_results[-1]
    if last_command["exit_code"] != 0:
        result.actually_passing = False
        result.notes.append(
            f"Verification failed: {last_command['command']}"
        )
        return result
    
    result.actually_passing = True
    result.tests_run = True

    return result