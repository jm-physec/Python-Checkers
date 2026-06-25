# v1.0 of the AI for the game, maybe I'll improve it if future version of the game comes

import math

from checkers import possible_moves, has_captures, COLUMNS, ROWS


def capture_moves(board, row, col, color):
    return [m for m in possible_moves(board, row, col, color) if m[2]]


def evaluate(board, ai_color):
    # Kings count as 3 pieces
    opp_color = "b" if ai_color == "w" else "w"
    score = 0
    for row in board:
        for p in row:
            if p == ".":
                continue
            value = 3 if p.isupper() else 1
            if p.lower() == ai_color:
                score += value
            elif p.lower() == opp_color:
                score -= value
    return score


def _silent_apply(board, origin, dest, is_capture, color):
    # Copy of apply_move without prints
    r_o, c_o = origin
    r_d, c_d = dest
    piece = board[r_o][c_o]
    board[r_d][c_d] = piece
    board[r_o][c_o] = "."
    if is_capture:
        board[(r_o + r_d) // 2][(c_o + c_d) // 2] = "."
    if piece.islower():
        if (color == "w" and r_d == 0) or (color == "b" and r_d == 7):
            board[r_d][c_d] = piece.upper()


def capture_sequences(board, origin, first_capture, color):
    # Explore all possible multi-jumps
    nr, nc, _ = first_capture
    board_copy = [row[:] for row in board]
    _silent_apply(board_copy, origin, (nr, nc), True, color)
    step = (origin, (nr, nc), True)

    next_caps = capture_moves(board_copy, nr, nc, color)
    if not next_caps:
        return [[step]]

    sequences = []
    for cap in next_caps:
        for sub in capture_sequences(board_copy, (nr, nc), cap, color):
            sequences.append([step] + sub)
    return sequences


def legal_turns(board, color):
    if has_captures(board, color):
        turns = []
        for r in range(8):
            for c in range(8):
                if board[r][c].lower() == color:
                    for cap in capture_moves(board, r, c, color):
                        turns.extend(capture_sequences(board, (r, c), cap, color))
        return turns

    turns = []
    for r in range(8):
        for c in range(8):
            if board[r][c].lower() == color:
                for m in possible_moves(board, r, c, color):
                    turns.append([((r, c), (m[0], m[1]), m[2])])
    return turns


def _apply_turn(board, turn, color):
    #Apply a full turn (possibly several jumps) to a board copy.
    new_board = [row[:] for row in board]
    for origin, dest, is_capture in turn:
        _silent_apply(new_board, origin, dest, is_capture, color)
    return new_board


def minimax(board, depth, color, ai_color, alpha, beta):
    opponent = "b" if color == "w" else "w"
    turns = legal_turns(board, color)

    if not turns:
        # Lost position
        return (-10000 if color == ai_color else 10000), None

    if depth == 0:
        return evaluate(board, ai_color), None

    maximizing = (color == ai_color)
    best_turn = turns[0]

    if maximizing:
        best_score = -math.inf
        for turn in turns:
            new_board = _apply_turn(board, turn, color)
            score, _ = minimax(new_board, depth - 1, opponent, ai_color, alpha, beta)
            if score > best_score:
                best_score, best_turn = score, turn
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return best_score, best_turn
    else:
        best_score = math.inf
        for turn in turns:
            new_board = _apply_turn(board, turn, color)
            score, _ = minimax(new_board, depth - 1, opponent, ai_color, alpha, beta)
            if score < best_score:
                best_score, best_turn = score, turn
            beta = min(beta, score)
            if alpha >= beta:
                break
        return best_score, best_turn


def choose_turn(board, color, depth=8):
    _, turn = minimax(board, depth, color, color, -math.inf, math.inf)
    return turn


def format_move(origin, dest):
    return f"{ROWS[origin[0]]}{COLUMNS[origin[1]]} -> {ROWS[dest[0]]}{COLUMNS[dest[1]]}"
