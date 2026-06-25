# Console Checkers - simple two-player version
# Terminal only, no libs needed.
# v2.0 AI implemented (change AI_DEPTH for more/less difficulty)
# TODO: Unlimited squares in king's movements (not only one)
# TODO: Maybe GUI? It's complicated, may be implemented in next version if it comes

import random

COLUMNS = "ABCDEFGH"
ROWS = "12345678"
AI_DEPTH = 8


def draw_board(board):
    print("   " + " ".join(COLUMNS))
    for i in range(len(board)):
        row = board[i]
        print(f"{i + 1}  " + " ".join(row))


def valid_name(name):
    return 6 <= len(name) <= 12 and all(c.isalnum() for c in name)


def ask_name(player_number):
    while True:
        name = input(f"Hey Player {player_number}, what's your name? (6-12 chars): ").strip()
        if valid_name(name):
            return name
        print("Invalid name, go again (6-12 letters/nums).")


def cell_to_coord(cell_text):
    cell_text = cell_text.strip().upper()
    if len(cell_text) != 2:
        return None
    row_char, col_char = cell_text[0], cell_text[1]
    if row_char not in ROWS or col_char not in COLUMNS:
        return None
    row = int(row_char) - 1
    col = COLUMNS.index(col_char)
    return row, col


def create_board():
    board = [["." for _ in range(8)] for _ in range(8)]
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = "b"
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = "w"
    return board


def forward_directions(piece):
    if piece.lower() == "w":
        return [-1] if piece.islower() else [-1, 1]
    else:
        return [1] if piece.islower() else [-1, 1]


def possible_moves(board, row, col, color):
    piece = board[row][col]
    if piece == "." or piece.lower() != color:
        return []

    moves = []
    for dv in forward_directions(piece):
        for dh in (-1, 1):
            nr, nc = row + dv, col + dh
            if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == ".":
                moves.append((nr, nc, False))

            nr2, nc2 = row + 2 * dv, col + 2 * dh
            if 0 <= nr2 < 8 and 0 <= nc2 < 8 and board[nr2][nc2] == ".":
                middle = board[row + dv][col + dh]
                if middle != "." and middle.lower() != color:
                    moves.append((nr2, nc2, True))
    return moves


def capture_moves_from(board, row, col, color):
    return [m for m in possible_moves(board, row, col, color) if m[2]]


def has_legal_move(board, color):
    for r in range(8):
        for c in range(8):
            if board[r][c].lower() == color:
                if possible_moves(board, r, c, color):
                    return True
    return False


def has_captures(board, color):
    for r in range(8):
        for c in range(8):
            if board[r][c].lower() == color:
                if capture_moves_from(board, r, c, color):
                    return True
    return False


def apply_move(board, origin, destination, is_capture, color):
    r_o, c_o = origin
    r_d, c_d = destination
    piece = board[r_o][c_o]
    board[r_d][c_d] = piece
    board[r_o][c_o] = "."
    if is_capture:
        board[(r_o + r_d) // 2][(c_o + c_d) // 2] = "."
    if piece.islower():
        if (color == "w" and r_d == 0) or (color == "b" and r_d == 7):
            board[r_d][c_d] = piece.upper()
            print(f"{color.upper()} piece promoted to King!!")


def commands(command, player_data):
    cmd = command.lower()

    if cmd in {"!hello", "!hi"}:
        print("Hello!!! I'm just a script, no feelings here. :)")
        return "OK"

    if cmd == "!end":
        print("Game ended by player request.")
        return "END"

    if cmd in {"!changename", "!cn"}:
        if player_data["name_changes"] >= 2:
            print("You've already used both name changes... Go and finish the game.")
            return "OK"
        while True:
            new_name = input("New name (6-12 alphanumeric): ").strip()
            if valid_name(new_name):
                player_data["name"] = new_name
                player_data["name_changes"] += 1
                print(f"Name changed to {new_name}.")
                break
            print("Invalid name / Nombre invalido")
        return "OK"

    if cmd in {"!changechar", "!cc"}:
        if player_data["char_changes"] >= 2:
            print("You've already used both character changes... Go play the game instead of this")
            return "OK"
        while True:
            new_char = input("New character (one UPPERCASE letter): ").strip().upper()
            if len(new_char) == 1 and new_char.isalpha() and new_char.isupper():
                if new_char == player_data["opponent_char"]:
                    print("That character is used by your opponent.")
                elif new_char == player_data["char"]:
                    print("You already use that character.")
                else:
                    player_data["char"] = new_char
                    player_data["char_changes"] += 1
                    print(f"Character changed to {new_char}.")
                    break
            else:
                print("Invalid character.")
        return "OK"

    return None


def do_multi_jump(board, r_d, c_d, current_color, current_turn, stats):
    while True:
        next_captures = capture_moves_from(board, r_d, c_d, current_color)
        if not next_captures:
            break

        print(f">> Multi-jump! {ROWS[r_d]}{COLUMNS[c_d]} can capture again.")
        draw_board(board)

        while True:
            entry = input(f"{current_turn}, next capture destination: ").strip()

            if entry.lower() == "!end":
                print("Game ended by player request.")
                return "END"

            destination = cell_to_coord(entry)
            if not destination:
                print("Wrong format.")
                continue

            chosen = None
            for nr, nc, cap in next_captures:
                if (nr, nc) == destination:
                    chosen = (nr, nc, cap)
                    break

            if not chosen:
                print("That's not a valid capture destination.")
                continue

            apply_move(board, (r_d, c_d), destination, True, current_color)
            stats["captured"][current_color] += 1
            r_d, c_d = destination
            break

    return None


def main():
    import ai  # local import: ai.py imports from this file, so importing it at module level here would create a circular import

    print("CONSOLE CHECKERS")
    print("Commands: !end | !changename (!cn) | !changechar (!cc)")
    print("Try typing !hi for a greeting!")
    print()

    mode = ""
    while mode not in {"1", "2"}:
        mode = input("Choose mode: [1] Human vs Human  [2] Human vs AI: ").strip()

    name1 = ask_name(1)
    if mode == "2":
        name2 = "AI"
    else:
        name2 = ask_name(2)

    if random.choice([True, False]):
        color_assignment = {name1: "w", name2: "b"}
    else:
        color_assignment = {name1: "b", name2: "w"}

    name_by_color = {v: k for k, v in color_assignment.items()}

    ai_color = color_assignment[name2] if mode == "2" else None

    print("\nColor draw:")
    print(f"  {name_by_color['w']} -> WHITE  (w / W for king)")
    print(f"  {name_by_color['b']} -> BLACK  (b / B for king)")
    print()

    board = create_board()
    draw_board(board)

    players = {
        name1: {
            "color": color_assignment[name1],
            "char": color_assignment[name1],
            "name_changes": 0,
            "char_changes": 0,
            "opponent_char": None,
        },
        name2: {
            "color": color_assignment[name2],
            "char": color_assignment[name2],
            "name_changes": 0,
            "char_changes": 0,
            "opponent_char": None,
        },
    }
    players[name1]["opponent_char"] = players[name2]["char"]
    players[name2]["opponent_char"] = players[name1]["char"]

    current_turn = name_by_color["w"]
    stats = {"turns": 0, "captured": {"w": 0, "b": 0}}

    while True:
        stats["turns"] += 1
        current_color = players[current_turn]["color"]
        opponent_color = "b" if current_color == "w" else "w"
        opponent_name = name_by_color[opponent_color]
        color_label = "WHITE" if current_color == "w" else "BLACK"

        print(f"Turn {stats['turns']}: {current_turn} ({color_label})")

        if ai_color is not None and current_color == ai_color:
            print(f"{current_turn} is thinking...")
            turn_sequence = ai.choose_turn(board, current_color, depth=AI_DEPTH)
            for origin, dest, is_capture in turn_sequence:
                move_text = ai.format_move(origin, dest)
                tag = " (capture)" if is_capture else ""
                print(f"{current_turn} plays {move_text}{tag}")
                apply_move(board, origin, dest, is_capture, current_color)
                if is_capture:
                    stats["captured"][current_color] += 1
            draw_board(board)

        else:
            captures_only = has_captures(board, current_color)
            if captures_only:
                print(">> Capture available, you must take it.")

            cmd_result = None
            while True:
                entry = input(f"{current_turn}, piece to move (e.g. 6A) or command: ").strip()
                cmd_result = commands(entry, players[current_turn])
                if cmd_result == "END":
                    break
                if cmd_result == "OK":
                    continue

                origin = cell_to_coord(entry)
                if not origin:
                    print(f"Bad format: '{entry}'. Try something like '6A' or '3H'.")
                    continue

                r_o, c_o = origin
                if board[r_o][c_o].lower() != current_color:
                    print("That cell doesn't have one of your pieces, try another one")
                    continue

                moves = possible_moves(board, r_o, c_o, current_color)
                if captures_only:
                    moves = [m for m in moves if m[2]]
                if not moves:
                    if captures_only:
                        print("That piece can't capture, pick another.")
                    else:
                        print("That piece has no moves.")
                    continue
                break

            if cmd_result == "END":
                break

            while True:
                entry = input(f"{current_turn}, destination (e.g. 5B) or command: ").strip()
                cmd_result = commands(entry, players[current_turn])
                if cmd_result == "END":
                    break
                if cmd_result == "OK":
                    continue

                destination = cell_to_coord(entry)
                if not destination:
                    print(f"Bad format: '{entry}'. Try something like '5B' or '4C'.")
                    continue

                legal = possible_moves(board, r_o, c_o, current_color)
                if captures_only:
                    legal = [m for m in legal if m[2]]

                chosen_move = None
                for nr, nc, capture in legal:
                    if (nr, nc) == destination:
                        chosen_move = (nr, nc, capture)
                        break

                if not chosen_move:
                    print("Move not allowed.")
                    continue
                break

            if cmd_result == "END":
                break

            apply_move(board, (r_o, c_o), destination, chosen_move[2], current_color)
            if chosen_move[2]:
                stats["captured"][current_color] += 1
                result = do_multi_jump(
                    board, destination[0], destination[1],
                    current_color, current_turn, stats
                )
                if result == "END":
                    break

            draw_board(board)

        whites = sum(p.lower() == "w" for row in board for p in row)
        blacks = sum(p.lower() == "b" for row in board for p in row)
        if whites == 0:
            print(f"GAME OVER. {name_by_color['b']} wins!")
            break
        if blacks == 0:
            print(f"GAME OVER. {name_by_color['w']} wins!")
            break

        if not has_legal_move(board, opponent_color):
            print(f"{opponent_name} has no legal moves. {current_turn} wins!")
            break

        current_turn = opponent_name

    print("\n=== STATISTICS ===")
    print(f"Turns played: {stats['turns']}")
    print(f"Captured -- White: {stats['captured']['w']}  Black: {stats['captured']['b']}")
    for player_name, data in players.items():
        print(
            f"  {player_name}: name changes {data['name_changes']}/2, "
            f"char changes {data['char_changes']}/2"
        )
    print("Thanks for playing!!")


if __name__ == "__main__":
    main()
