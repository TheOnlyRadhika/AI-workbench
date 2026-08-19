from task_board import initialize_board, load_board, save_board , get_next_task


initialize_board()

board = load_board()

print("Initial board:")
for task in board.tasks:
    print(task)

board.tasks[0].status = "in_progress"

save_board(board)

updated_board = load_board()

print("\nUpdated board:")
for task in updated_board.tasks:
    print(task)

next_task = get_next_task(board)
print("\nNext Task:")
print(next_task)