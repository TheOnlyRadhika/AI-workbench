from feedback import record_command_result, run_command
from handoff import create_handoff
from initializer import initialize_workbench
from models import RunResult
from reviewer import review_run
from state import load_state, save_state
from task_board import (
    complete_task,
    get_next_task,
    load_board,
    save_board,
)
from verifier import verify_run


def run_turn():
    initialize_workbench()

    state = load_state()
    board = load_board()

    # 1. Select a task
    if state.active_task is None:
        task = get_next_task(board)

        if task is None:
            print("No tasks available")
            return

        state.active_task = task.id
        task.status = "in_progress"

        save_state(state)
        save_board(board)

    else:
        # Resume the existing task
        task = next(
            task for task in board.tasks
            if task.id == state.active_task
        )


    # 2. Create a result for this run
    result = RunResult(
        label=state.active_task
    )

    # 3. Run a command
    command_result = run_command("python --version")

    # 4. Record runtime feedback
    record_command_result(result, command_result)

    # 5. Verify the run
    result = verify_run(result)
    review = review_run(task, result)


    # 6. Update task based on verification
    if result.actually_passing and review.approved:
        complete_task(board, state.active_task)
        state.active_task = None
        state.next_action = None
        print("Task completed")

    else:
        print("Task requires more work")
        state.blockers.extend(review.issues)
        state.next_action = "Fix the issues identified during verification and review"
        handoff = create_handoff(
            state,
            task,
            summary="Current run was not accepted."
        )
        print("\nHandoff:")
        print(handoff)

    save_board(board)
    save_state(state)

    # 7. Persist everything
    save_board(board)
    save_state(state)


if __name__ == "__main__":
    run_turn()