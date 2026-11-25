from models import Task

#from workbench import execute_github_task
from orchestrator import execute_task

task = Task(
    id="validate-csv-columns",
    description="""
    Improve read_csv_data in starter_repo/plot_data.py.

    If either the requested x or y column does not exist in the CSV,
    raise a ValueError with a clear message identifying the missing column.

    First inspect the existing implementation and tests.
    Add appropriate tests in tests/test_plot_data.py.
    Make the smallest necessary code change.
    Run the relevant tests after making the change.
    """,
    allowed_files=[
        "starter_repo/plot_data.py",
        "tests/test_plot_data.py"
    ],
    forbidden_files=[],
    acceptance=[
        "All tests pass",
        "Tests are actually run",
        "No scope violations",
        "Agent reports completion"
    ]
)


result, review, handoff = execute_task(
    task,
    "workdir/starter_repo"
)


print("\nRESULT:")
print(result)

print("\nREVIEW:")
print(review)

print("\nHANDOFF:")
print(handoff)