from models import Task
from agent import plan_task

task = Task(
    id = "add-big-fix",
    description="Add input validation to /signup",
    allowed_files=["app.py", "test_app.py"],
    forbidden_files=["README.md"],
    acceptance=[
        "Short passwords are rejected",
        "Signup validation test passes"
    ]
)

plan = plan_task(task)

print("\nAgent plan:")
print(plan)