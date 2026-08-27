from models import Task , TaskStatus
from orchestrator import execute_task


def test_execute_task():

    task = Task(
        id = "add-big-fix",
        description="""
        Fix the bug in the add function so that all tests in the repository pass.

        First inspect the relevant files.
        Then make the necessary code change.
        Finally run the tests to verify the fix.
        """,
        allowed_files=[
            "app.py",
            "test_app.py"
        ],
        forbidden_files=[],
        acceptance=[
            "All tests pass",
            "Tests are actually run",
            "No scope violations",
            "Agent reports completion"
        ]
    )

    result, review , handoff = execute_task(
        task,
        "workdir/demo_repo"
    )
    assert result.actually_passing is True
    assert review.approved is True
    assert handoff.task_id == task.id
    assert handoff.files_touched == result.files_touched
    assert task.status == TaskStatus.COMPLETED
    assert handoff.next_action == "Ready for handoff"


    print("RUN RESULT:", result.summary())
    print("REVIEW:", review)
    print("HANDOFF:", handoff)

    