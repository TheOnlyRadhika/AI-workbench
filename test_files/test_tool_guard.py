from models import Task
from tool_guard import check_tool_allowed


task = Task(
    id = "add-big-fix",
    description="Update signup validation",
    allowed_files=[
        "app.py",
        "test_app.py"
    ],
    forbidden_files=[
        "README.md"
    ],
    acceptance=[
        "Signup test passes"
    ]
)


print("Read allowed file:")
print(
    check_tool_allowed(
        "read_file",
        {"path": "app.py"},
        task
    )
)


print("\nRead forbidden file:")
print(
    check_tool_allowed(
        "read_file",
        {"path": "README.md"},
        task
    )
)


print("\nWrite allowed file:")
print(
    check_tool_allowed(
        "write_file",
        {
            "path": "app.py",
            "content": "new code"
        },
        task
    )
)


print("\nWrite forbidden file:")
print(
    check_tool_allowed(
        "write_file",
        {
            "path": "README.md",
            "content": "new content"
        },
        task
    )
)


print("\nList files:")
print(
    check_tool_allowed(
        "list_files",
        {"root": "."},
        task
    )
)


print("\nAllowed command:")
print(
    check_tool_allowed(
        "run_command",
        {"command": "pytest"},
        task
    )
)


print("\nRejected command:")
print(
    check_tool_allowed(
        "run_command",
        {"command": "rm -rf /"},
        task
    )
)