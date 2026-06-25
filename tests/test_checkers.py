import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checkers import (
    valid_name,
    cell_to_coord,
    create_board,
    forward_directions,
    possible_moves,
    capture_moves_from,
    has_legal_move,
    has_captures,
    apply_move,
    commands,
)


def empty_board():
    return [["." for _ in range(8)] for _ in range(8)]


# --- valid_name ---

def test_valid_name_accepts_correct_length():
    assert valid_name("player1")


def test_valid_name_rejects_too_short():
    assert not valid_name("abc")


def test_valid_name_rejects_too_long():
    assert not valid_name("waytoolongname123")


def test_valid_name_rejects_special_characters():
    assert not valid_name("player_1")


# --- cell_to_coord ---

def test_cell_to_coord_converts_correctly():
    assert cell_to_coord("6A") == (5, 0)


def test_cell_to_coord_handles_lowercase():
    assert cell_to_coord("6a") == (5, 0)


def test_cell_to_coord_handles_spaces():
    assert cell_to_coord("  6A  ") == (5, 0)


def test_cell_to_coord_rejects_bad_length():
    assert cell_to_coord("6AB") is None


def test_cell_to_coord_rejects_invalid_row():
    assert cell_to_coord("9A") is None


def test_cell_to_coord_rejects_invalid_column():
    assert cell_to_coord("6Z") is None


# --- create_initial_board ---

def test_initial_board_has_12_pieces_per_side():
    board = create_board()
    whites = sum(row.count("w") for row in board)
    blacks = sum(row.count("b") for row in board)
    assert whites == 12
    assert blacks == 12


def test_initial_board_pieces_only_on_dark_squares():
    board = create_board()
    for r in range(8):
        for c in range(8):
            if board[r][c] != ".":
                assert (r + c) % 2 == 1


# --- forward_directions ---

def test_regular_white_piece_moves_up_only():
    assert forward_directions("w") == [-1]


def test_regular_black_piece_moves_down_only():
    assert forward_directions("b") == [1]


def test_king_moves_both_directions():
    assert forward_directions("W") == [-1, 1]
    assert forward_directions("B") == [-1, 1]


# --- possible_moves ---

def test_possible_moves_empty_cell_returns_nothing():
    board = create_board()
    assert possible_moves(board, 3, 3, "w") == []


def test_possible_moves_simple_move_available():
    board = empty_board()
    board[4][4] = "w"
    moves = possible_moves(board, 4, 4, "w")
    assert (3, 3, False) in moves
    assert (3, 5, False) in moves


def test_possible_moves_detects_capture():
    board = empty_board()
    board[4][4] = "w"
    board[3][3] = "b"
    moves = possible_moves(board, 4, 4, "w")
    assert (2, 2, True) in moves


def test_possible_moves_no_capture_if_landing_blocked():
    board = empty_board()
    board[4][4] = "w"
    board[3][3] = "b"
    board[2][2] = "w"
    moves = possible_moves(board, 4, 4, "w")
    assert (2, 2, True) not in moves


def test_possible_moves_wrong_color_returns_nothing():
    board = empty_board()
    board[4][4] = "w"
    assert possible_moves(board, 4, 4, "b") == []


# --- capture_moves_from ---

def test_capture_moves_from_filters_non_captures():
    board = empty_board()
    board[4][4] = "w"
    board[3][3] = "b"
    captures = capture_moves_from(board, 4, 4, "w")
    assert captures == [(2, 2, True)]


# --- has_legal_move ---

def test_has_legal_move_true_when_piece_has_moves():
    board = empty_board()
    board[4][4] = "w"
    assert has_legal_move(board, "w")


def test_has_legal_move_false_when_no_pieces():
    board = empty_board()
    assert not has_legal_move(board, "w")


def test_has_legal_move_false_when_stuck_at_edge():
    board = empty_board()
    # Regular white piece moves toward row 0; placed there it has
    # nowhere left to go (off-board), and it isn't a king.
    board[0][3] = "w"
    assert not has_legal_move(board, "w")


# --- has_captures ---

def test_has_captures_true_when_jump_available():
    board = empty_board()
    board[4][4] = "w"
    board[3][3] = "b"
    assert has_captures(board, "w")


def test_has_captures_false_when_no_jump_available():
    board = empty_board()
    board[4][4] = "w"
    assert not has_captures(board, "w")


# --- apply_move ---

def test_apply_move_moves_piece():
    board = empty_board()
    board[4][4] = "w"
    apply_move(board, (4, 4), (3, 3), False, "w")
    assert board[4][4] == "."
    assert board[3][3] == "w"


def test_apply_move_removes_captured_piece():
    board = empty_board()
    board[4][4] = "w"
    board[3][3] = "b"
    apply_move(board, (4, 4), (2, 2), True, "w")
    assert board[3][3] == "."
    assert board[2][2] == "w"


def test_apply_move_promotes_white_to_king_on_row_0():
    board = empty_board()
    board[1][1] = "w"
    apply_move(board, (1, 1), (0, 0), False, "w")
    assert board[0][0] == "W"


def test_apply_move_promotes_black_to_king_on_row_7():
    board = empty_board()
    board[6][1] = "b"
    apply_move(board, (6, 1), (7, 0), False, "b")
    assert board[7][0] == "B"


def test_apply_move_does_not_crash_on_existing_king():
    board = empty_board()
    board[1][1] = "W"
    apply_move(board, (1, 1), (0, 0), False, "w")
    assert board[0][0] == "W"


# --- process_command ---

def test_process_command_end_returns_end():
    player_data = {"name_changes": 0, "char_changes": 0, "char": "w", "opponent_char": "b"}
    assert commands("!end", player_data) == "END"


def test_process_command_unknown_text_returns_none():
    player_data = {"name_changes": 0, "char_changes": 0, "char": "w", "opponent_char": "b"}
    assert commands("6A", player_data) is None


def test_process_command_hi_returns_ok():
    player_data = {"name_changes": 0, "char_changes": 0, "char": "w", "opponent_char": "b"}
    assert commands("!hi", player_data) == "OK"


def test_process_command_changename_blocked_after_limit():
    player_data = {"name_changes": 2, "char_changes": 0, "char": "w", "opponent_char": "b"}
    assert commands("!cn", player_data) == "OK"
    assert player_data["name_changes"] == 2
