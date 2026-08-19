from state import initialize_state, load_state, save_state


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