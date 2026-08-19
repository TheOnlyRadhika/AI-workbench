from dataclasses import dataclass
import subprocess
from models import RunResult , CommandResult
    
def record_command_result(run_result : RunResult, command_result: CommandResult)-> RunResult:
    run_result.command_results.append({
        "command": command_result.command,
        "stdout": command_result.stdout,
        "stderr": command_result.stderr,
        "exit_code": command_result.exit_code,
        "passed": command_result.passed
    })
    return run_result



def run_command(command: str) -> CommandResult:
    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )

    return CommandResult(
        command=command,
        stdout=process.stdout,
        stderr=process.stderr,
        exit_code=process.returncode,
    )