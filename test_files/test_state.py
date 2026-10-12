from state import initialize_state, load_state, save_state
from state import set_active_task


initialize_state()

state = load_state()

print("Initial state:")
print(state)

state.active_task = "signup-validation"
state.touched_files.append("app.py")
state.next_action = "Run pytest"

save_state(state)

updated_state = load_state()

print("\nUpdated state:")
print(updated_state)


def test_set_active_task(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    initialize_state()

    state = load_state()

    set_active_task(state, "test-task")

    loaded_state = load_state()

    assert loaded_state.active_task == "test-task"
    assert loaded_state.next_action == "Task execution pending"
    assert loaded_state.last_updated is not None