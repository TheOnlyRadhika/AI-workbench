from models import Task, RunResult , ScopeContract

def check_file_allowed(contract: ScopeContract, file: str) -> bool:
    if file in contract.forbidden_files:
        return False
    return file in contract.allowed_files


def validate_files(contract: ScopeContract, files: list[str]) -> list[str]:
    violations = []
    for file in files:
        if not check_file_allowed(contract, file):
            violations.append(file)

    return violations


def check_run_scope(contract:ScopeContract, result: RunResult) -> RunResult:
    result.scope_violations = validate_files(contract , result.files_touched)
    if result.scope_violations:
        result.notes.append(f"scope violations: {result.scope_violations}")
    return result


def create_scope_contract(task:Task) -> ScopeContract:
    return ScopeContract(
        allowed_files = task.allowed_files,
        forbidden_files = task.forbidden_files
    )