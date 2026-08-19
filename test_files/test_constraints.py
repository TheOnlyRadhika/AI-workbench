from models import Task , RunResult , ScopeContract
from constraints import check_file_allowed , check_run_scope, create_scope_contract, validate_files


task = Task(
    description="Add input validation to /signup",
    allowed_files=["app.py", "test_app.py"],
    forbidden_files=["README.md", "scripts/release.sh"],
    acceptance=["Signup test passes"],
)
contract = create_scope_contract(task)

print(check_file_allowed(contract, "app.py"))
print(check_file_allowed(contract, "README.md"))
print(check_file_allowed(contract, "scripts/release.sh"))


valid_result = RunResult(
    label="valid-run",
    files_touched=["app.py", "test_app.py"]
)
check_run_scope(task, valid_result)
print("\nValid result:")
print(valid_result)

invalid_result = RunResult(
    label="invalid-run",
    files_touched=["app.py", "README.md", "scripts/release.sh"]
)
check_run_scope(task, invalid_result)
print("\nInvalid result:")
print(invalid_result)

violations = validate_files(
    contract,
    valid_result.files_touched
)
print("Scope violations:")
print(violations)