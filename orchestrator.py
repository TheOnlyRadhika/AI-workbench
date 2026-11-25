from agent import run_agent
from handoff import create_handoff
from models import TaskStatus
from reviewer import review_run
from state import initialize_state, load_state, save_state
from task_board import initialize_board, load_board, save_board, update_task_status
from verifier import verify_run


def execute_task(task, repo_root):
    initialize_board()
    board = load_board()
    update_task_status(
        board,
        task.id,
        TaskStatus.RUNNING.value,
    )
    save_board(board)

    # Task has started
    task.status = TaskStatus.RUNNING

    initialize_state()
    state = load_state()
    state.active_task = task.id
    state.next_action = "Running task"
    save_state(state)

    try:
        result = run_agent(task, repo_root)
        result = verify_run(result, task)
        review = review_run(task, result)
    except Exception as exc:
        task.status = TaskStatus.FAILED
        state.next_action = "Task execution failed"
        state.blockers = [str(exc)]

        update_task_status(
            board,
            task.id,
            TaskStatus.FAILED.value,
        )
        save_board(board)
        save_state(state)
        raise

    # Update task lifecycle based on review
    if review.approved:
        task.status = TaskStatus.COMPLETED
        state.next_action = "Ready for handoff"

        update_task_status(
            board,
            task.id,
            TaskStatus.COMPLETED.value,
        )
    else:
        task.status = TaskStatus.FAILED
        state.next_action = "Requires further work"
        state.blockers = review.issues

        update_task_status(
            board,
            task.id,
            TaskStatus.FAILED.value,
        )
    state.touched_files = result.files_touched

    save_board(board)
    save_state(state)
    handoff_summary = {
        "status": "approved" if review.approved else "rejected",
        "tests_run": result.tests_run,
        "actually_passing": result.actually_passing,
        "declared_success": result.declared_success,
        "review_issues": review.issues,
        "review_notes": review.notes,
    }

    try:
        handoff = create_handoff(state, task, handoff_summary)

    except Exception as exc:
        state.blockers.append(
            f"Handoff generation failed: {exc}"
        )
        state.next_action = "Retry handoff generation"
        save_state(state)
        handoff = None

    return result, review, handoff
