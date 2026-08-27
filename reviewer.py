from models import Task, RunResult , ReviewResult

def review_run(task: Task, result: RunResult) -> ReviewResult:

    issues = []
    notes = []

    if result.scope_violations:
        issues.append(
            f"Scope violations: {result.scope_violations}"
        )
    if not result.actually_passing:
        issues.append(
            "Verification did not pass"
        )
    if not issues:
        notes.append(
            "Run passed scope and verification checks."
        )
    return ReviewResult(
        approved=len(issues) == 0,
        issues=issues,
        notes=notes,
    )