
import argparse
import sys
from pprint import pprint

from workbench import run_workbench


def main():
    parser = argparse.ArgumentParser(
        description="Agentic AI Workbench: execute a coding task on a GitHub repository."
    )

    parser.add_argument("--repo-url", required=True, help="GitHub repository URL")
    parser.add_argument("--workspace", required=True, help="Local clone destination")
    parser.add_argument("--task-id", required=True, help="Unique task ID")
    parser.add_argument("--description", required=True, help="Coding task description")

    parser.add_argument(
        "--allowed-files",
        nargs="+",
        required=True,
        help="Files the agent is allowed to modify",
    )
    parser.add_argument(
        "--acceptance",
        nargs="+",
        required=True,
        help="Acceptance criteria for the task",
    )
    parser.add_argument(
        "--forbidden-files",
        nargs="*",
        default=[],
        help="Files the agent must not modify",
    )

    args = parser.parse_args()

    try:
        result, review, handoff = run_workbench(
            repo_url=args.repo_url,
            workspace=args.workspace,
            task_id=args.task_id,
            description=args.description,
            allowed_files=args.allowed_files,
            acceptance=args.acceptance,
            forbidden_files=args.forbidden_files,
        )

        print("\n=== Execution Result ===")
        pprint(result)

        print("\n=== Review ===")
        pprint(review)

        print("\n=== Handoff ===")
        pprint(handoff)

        return 0 if review.approved else 1

    except Exception as exc:
        print(f"Workbench failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
