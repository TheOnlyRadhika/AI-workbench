from models import RunResult, Task
from reviewer import review_run


def test_review_success():

    task = Task(
        id = "add-big-fix",
        description="Fix bug",
        allowed_files=["app.py"],
        forbidden_files=[],
        acceptance=["All tests pass"]
    )

    result = RunResult(
        label="test",
        files_touched=["app.py"],
        actually_passing=True
    )

    review = review_run(task, result)

    assert review.approved is True
    assert review.issues == []



def test_review_verification_failure():
    task = Task(
        id = "add-big-fix",
        description="Fix bug",
        allowed_files=["app.py"],
        forbidden_files=[],
        acceptance=["All tests pass"]
    )

    result = RunResult(
        label="test",
        files_touched=["app.py"],
        actually_passing=False
    )

    review = review_run(task, result)
    assert review.approved is False
    assert "Verification did not pass" in review.issues



def test_review_scope_violation():
    task = Task(
        id = "add-big-fix",
        description="Fix bug",
        allowed_files=["app.py"],
        forbidden_files=[],
        acceptance=["All tests pass"]
    )

    result = RunResult(
        label="test",
        files_touched=["app.py", "README.md"],
        actually_passing=True,
        scope_violations=["README.md"]
    )

    review = review_run(task, result)
    assert review.approved is False
    assert review.issues