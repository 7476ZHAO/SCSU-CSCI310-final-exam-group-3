import threading, random, time
from character import Character

# --- Game setup ---
BOARD_SIZE = 5  # ✅ fixed 5x5 grid

mountain_location = [random.randint(0,4),random.randint(0,4)]

board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
game_over = False

board [mountain_location[0]] [mountain_location[1]] = "M"

lock = threading.Lock()
barrier = threading.Barrier(4)  # 4 players total

# Create 4 Character objects
players = {
    "B": Character(random.randint(0, 4), random.randint(0, 4), "B", BOARD_SIZE),
    "T": Character(random.randint(0, 4), random.randint(0, 4), "T", BOARD_SIZE),
    "M": Character(random.randint(0, 4), random.randint(0, 4), "M", BOARD_SIZE),
    "D": Character(random.randint(0, 4), random.randint(0, 4), "D", BOARD_SIZE),
}

# Place initial characters on the board
for p in players.values():
    board[p.row][p.column] = p.name

# --- Helper functions ---
def print_board():
    for row in board:
        print(' | '.join(row))
        print('-' * (BOARD_SIZE * 4 - 3))
    print()

def check_winner(character):
    # Win rule: reaching top-left corner (0, 0)
    return character.row == 0 and character.column == 0

def take_turn(player_id):
    global game_over
    character = players[player_id]

    while not game_over:
        with lock:

            # Randomly move or teleport
            if random.random() < 0.8:
                character.move()
                if [character.row, character.column] == mountain_location:
                    character.move()
            else:
                character.teleport()
                if [character.row, character.column] == mountain_location:
                    character.move()

            # Clear old position
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if board[r][c] == player_id:
                        board[r][c] = ' '

            # Place new position
            board[character.row][character.column] = player_id

        # Wait for all players to move
        barrier.wait()

        # Print the board after everyone moves
        if barrier.broken or barrier.n_waiting == 0:
            with lock:
                print(f"\n=== All players moved! ===")
                print_board()

        # Win check
        if check_winner(character):
            with lock:
                print(f"🎉 Game Over! Player {player_id} wins!")
            game_over = True
            break

        time.sleep(1)

# --- Start threads ---
threads = [threading.Thread(target=take_turn, args=(pid,)) for pid in players]
for t in threads:
    t.start()
for t in threads:
    t.join()
