from models import HandOffPacket


def create_handoff(state, task , summary: dict)-> HandOffPacket:
    return HandOffPacket(
        task_id = task.id,
        summary = summary,
        files_touched = state.touched_files,
        blockers = state.blockers,
        next_action = state.next_action,
    )