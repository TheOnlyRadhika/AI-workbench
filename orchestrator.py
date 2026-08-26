from agent import run_agent
from verifier import verify_run
from reviewer import review_run
from handoff import create_handoff
from models import AgentState


def execute_task(task, repo_root):

    state = AgentState(
        active_task=task.id
    )

    result = run_agent(task, repo_root)
    result = verify_run(result, task)
    review = review_run(task, result)

    state.touched_files = result.files_touched
    if review.approved:
        state.next_action = "Ready for handoff"
    else:
        state.next_action = "Requires further work"
        state.blockers = review.issues

    handoff_summary = {
        "status": "approved" if review.approved else "rejected",
        "tests_run": result.tests_run,
        "actually_passing": result.actually_passing,
        "declared_success": result.declared_success,
        "review_issues": review.issues,
        "review_notes": review.notes,
    }

    handoff = create_handoff(
        state,
        task,
        handoff_summary
    )

    return result, review, handoff