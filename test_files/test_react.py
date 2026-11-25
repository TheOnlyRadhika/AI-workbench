from agent import run_agent
from models import Task

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
repo_root ="workdir/demo_repo"
result = run_agent(task , repo_root)
print("\nFINAL AGENT RESPONSE:")
print(result.summary())