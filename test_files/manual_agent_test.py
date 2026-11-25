from agent import plan_task
from models import Task


def test_plan_task():
    task = Task(
        id="add-big-fix",
        description="Add input validation to /signup",
        allowed_files=["app.py", "test_app.py"],
        forbidden_files=["README.md"],
        acceptance=[
            "Short passwords are rejected",
            "Signup validation test passes"
        ]
    )

    plan = plan_task(task)

    assert plan