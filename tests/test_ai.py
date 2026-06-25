import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai import (
    evaluate,
    get_legal_turns,
    choose_turn,
    get_forced_moves,
)


def empty_board():
    return [["." for _ in range(8)] for _ in range(8)]


# --- evaluate ---

def test_evaluate_zero_on_equal_material():
    board = empty_board()
    board[4][4] = "w"
    board[3][3] = "b"
    assert evaluate(board, "w") == 0


def test_evaluate_positive_when_ai_has_more_pieces():
    board = empty_board()
    board[4][4] = "w"
    board[5][5] = "w"
    board[3][3] = "b"
    assert evaluate(board, "w") > 0


def test_evaluate_kings_worth_more_than_regular_pieces():
    board = empty_board()
    board[4][4] = "W"
    score_with_king = evaluate(board, "w")
    board2 = empty_board()
    board2[4][4] = "w"
    score_with_regular = evaluate(board2, "w")
    assert score_with_king > score_with_regular


# --- get_legal_turns ---

def test_get_legal_turns_returns_simple_moves_when_no_capture():
    board = empty_board()
    board[4][4] = "w"
    turns = get_legal_turns(board, "w")
    # two diagonal moves available, no captures forced
    assert len(turns) == 2
    for turn in turns:
        assert len(turn) == 1
        assert turn[0][2] is False  # not a capture


def test_get_legal_turns_forces_capture_when_available():
    board = empty_board()
    board[4][4] = "w"
    board[3][3] = "b"
    turns = get_legal_turns(board, "w")
    # only the capturing move should be offered, not the other diagonal
    assert len(turns) == 1
    assert turns[0][0][2] is True


def test_get_legal_turns_includes_multi_jump_chain():
    board = empty_board()
    board[6][2] = "w"
    board[5][3] = "b"
    board[3][3] = "b"
    turns = get_legal_turns(board, "w")
    # at least one turn should have 2 steps (a double jump)
    assert any(len(t) == 2 for t in turns)


def test_get_legal_turns_empty_when_no_pieces():
    board = empty_board()
    assert get_legal_turns(board, "w") == []


# --- choose_turn ---

def test_choose_turn_takes_available_capture():
    board = empty_board()
    board[4][4] = "w"
    board[3][3] = "b"
    turn = choose_turn(board, "w", depth=2)
    assert turn is not None
    assert turn[0][2] is True  # the AI took the forced capture


def test_choose_turn_returns_none_when_no_moves():
    board = empty_board()
    board[0][1] = "w"  # stuck at the edge, regular piece, no moves
    turn = choose_turn(board, "w", depth=2)
    assert turn is None


def test_choose_turn_prefers_winning_capture_over_ignoring_material():
    # White can capture a black piece; with any reasonable depth it should.
    board = empty_board()
    board[4][4] = "w"
    board[5][5] = "w"
    board[3][3] = "b"
    turn = choose_turn(board, "w", depth=3)
    assert turn is not None
    assert any(step[2] for step in turn)
