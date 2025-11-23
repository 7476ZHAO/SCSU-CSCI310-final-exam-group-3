import threading, random, time
from character import Character

# --- Game setup ---
BOARD_SIZE = 5
CARROT_SYMBOL = "C"
MOUNTAIN_SYMBOL = "F"
NUM_CARROTS = 2

game_over = False
lock = threading.Lock()

# Track if player is alive
player_ids = ["B", "T", "M", "D"]
is_alive = {pid: True for pid in player_ids}# dic comprehension

# Mountain location
mountain_location = [
    random.randint(0, BOARD_SIZE - 1),
    random.randint(0, BOARD_SIZE - 1),
]

# Carrot locations
def get_free_location(exclude_locations):
    while True:
        pos = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]
        if pos not in exclude_locations:
            return pos

carrot_locations = []
exclude = [mountain_location]

#grab two random pos for carrots
for _ in range(NUM_CARROTS):
    pos = get_free_location(exclude)
    carrot_locations.append(pos)
    exclude.append(pos)

# Board
board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
board[mountain_location[0]][mountain_location[1]] = MOUNTAIN_SYMBOL
for c in carrot_locations:
    board[c[0]][c[1]] = CARROT_SYMBOL

# Player positions
current_locations = {"mountain": mountain_location.copy()}
players = {}

for pid in player_ids:
    pos = get_free_location(exclude + list(current_locations.values()))
    current_locations[pid] = pos
    players[pid] = Character(pos[0], pos[1], pid, BOARD_SIZE)#define a new charactor with row, column, name, board_size as a value in dic player
    board[pos[0]][pos[1]] = pid

player_cycles = {pid: 0 for pid in player_ids}


# --- Helper functions ---
def print_board():
    for row in board:
        print(" | ".join(row))
        print("-" * (BOARD_SIZE * 4 - 3))
    print("\n")


def check_winner(character):
    return (
        character.has_carrot
        and [character.row, character.column] == mountain_location
    )


def get_valid_moves(character, pid):
    moves = []
    occupied = {
        tuple(current_locations[p])
        for p in player_ids
        if p != pid and is_alive[p]
    }

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue

            new_row = max(0, min(character.row + dr, BOARD_SIZE - 1))
            new_col = max(0, min(character.column + dc, BOARD_SIZE - 1))

            # Can't step on mountain unless carrying carrot
            if [new_row, new_col] == mountain_location and not character.has_carrot:
                continue

            # Can't step on another player
            if (new_row, new_col) in occupied:
                continue

            moves.append([new_row, new_col])

    if not moves:
        return [[character.row, character.column]]

    return moves


def get_empty_location():
    while True:
        pos = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]
        if (
            pos not in current_locations.values()
            and pos not in carrot_locations
        ):
            return pos


def teleport_mountain():
    global mountain_location
    new_pos = get_empty_location()

    # Clear old mountain
    board[mountain_location[0]][mountain_location[1]] = " "

    mountain_location = new_pos
    board[new_pos[0]][new_pos[1]] = MOUNTAIN_SYMBOL

    print(f"Mountain teleported to {new_pos}!")


# --- Game loop ---
def take_turn(player_id):
    global game_over

    character = players[player_id]

    while not game_over:

        # Dead players immediately stop
        if not is_alive[player_id]:
            return

        with lock:#Run the code inside the block, release the lock when done
            player_cycles[player_id] += 1

        # M teleports mountain every 3 cycles
        if player_id == "M" and player_cycles[player_id] % 3 == 0:
            with lock:
                teleport_mountain()

        # Choose movement
        moves = get_valid_moves(character, player_id)
        new_pos = random.choice(moves)
        character.row, character.column = new_pos

        # Check if M kills someone
        if player_id == "M":
            with lock:
                for pid in player_ids:
                    if pid != "M" and is_alive[pid]:
                        if current_locations.get(pid) == [character.row, character.column]:

                            print(f"M killed {pid} at {new_pos}!")

                            # Steal carrot
                            if players[pid].has_carrot:
                                players["M"].has_carrot = True
                                players["M"].name = "M(C)"
                                print("M stole a carrot!")

                            # Kill player
                            is_alive[pid] = False
                            board[current_locations[pid][0]][current_locations[pid][1]] = " "
                            del current_locations[pid]
                            break

        # Check carrot pickup, if picked up, update player's name with adding "C"
        for carrot in list(carrot_locations):  # iterate on copy to safely remove
            if carrot == [character.row, character.column]:
                character.pick_carrot()  # changes name to M(C), B(C), etc.
                print(f"{character.name} picked a carrot!\n")
                print()
                carrot_locations.remove(carrot)
                # Update board immediately
                board[character.row][character.column] = character.name
                break

        # Update position on board, move the player from old position to new position
        with lock:
            old = current_locations.get(player_id)#The function get can retrive the value for key "player_id"
            if old:
                board[old[0]][old[1]] = " "
            current_locations[player_id] = [character.row, character.column]
            board[character.row][character.column] = character.name

            # Restore mountain and carrots
            board[mountain_location[0]][mountain_location[1]] = MOUNTAIN_SYMBOL
            for c in carrot_locations:
                board[c[0]][c[1]] = CARROT_SYMBOL

            print_board()

        # Check winner
        if check_winner(character):
            with lock:
                print(f"GAME OVER: {character.name} wins by reaching mountain with a carrot!")
                game_over = True
            return

        time.sleep(1)


# --- Start threads ---
threads = [threading.Thread(target=take_turn, args=(pid,)) for pid in player_ids]

for t in threads:
    t.start()

for t in threads:
    t.join()
