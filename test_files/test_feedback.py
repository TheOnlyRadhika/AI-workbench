from feedback import run_command

# run_result = RunResult(label="feedback-test")
# command_result = run_command("python --version")
# record_command_result(run_result, command_result)
# print(run_result)


repo_root = "workdir/demo_repo"

result = run_command(
    "pytest",
    repo_root
)

print(result)