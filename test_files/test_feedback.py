from models import RunResult
from feedback import run_command, record_command_result

run_result = RunResult(label="feedback-test")
command_result = run_command("python --version")
record_command_result(run_result, command_result)
print(run_result)