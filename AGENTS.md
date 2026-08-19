# Agent Instructions

## Before working

Read:

- `workdir/agent_state.json` — current agent state
- `workdir/task_board.json` — project task board

## Project rules

- Follow the task scope.
- Only modify files explicitly allowed by the active task.
- Do not modify forbidden files.
- Record important state changes in `workdir/agent_state.json`.

## Verification

Run the project's tests before declaring a task complete.

## Task completion

A task is complete only when its acceptance criteria have been verified.