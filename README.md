# Python-checkers

A two-player checkers game that runs in the terminal. I built this as a programming exercise. It's not fancy but it works — full rules, mandatory captures, multi-jumps, and king promotion.

Pure Python. No installs needed for the base game (pytest is only needed if you want to run the tests).

## Running it

```
python checkers.py
```

Python 3.8 or higher.

At the start you choose the mode:

```
Choose mode: [1] Human vs Human  [2] Human vs AI
```

## Controls

Moves are entered as row + column: select your piece first (e.g. `6A`), then the destination (e.g. `5B`).

```
   A B C D E F G H
1  . b . b . b . b
2  b . b . b . b .
3  . b . b . b . b
4  . . . . . . . .
5  . . . . . . . .
6  w . w . w . w .
7  . w . w . w . w
8  w . w . w . w .
```

White uses `w`, black uses `b`. Kings are uppercase (`W`, `B`).

A few things to know:
- Captures are mandatory. If you can take a piece, you have to.
- Multi-jumps work — after a capture, if the same piece can keep jumping, it does.
- Kings move all four diagonal directions (one square at a time, I kept it simple).

## Playing against the AI

Pick mode `2` at the start. Colors are still assigned randomly, so the AI might end up white or black either way.

The AI uses minimax search with alpha-beta pruning, looking 5 moves ahead by default (`AI_DEPTH` at the top of `checkers.py`, change it if you want it weaker/stronger — depth 6-7 is still nearly instant, depth 8+ starts noticeably slowing down).

It evaluates positions by material: regular pieces are worth 1 point, kings 3. It respects the same mandatory-capture and multi-jump rules as a human player — when it has a forced capture chain available, the whole chain is decided and played as one turn, not one jump at a time.

The search logic lives in `ai.py`, separate from the game engine in `checkers.py`.

## In-game commands

Type these instead of a cell at any prompt:

- `!end` — quit
- `!changename` or `!cn` — change your display name (up to twice)
- `!changechar` or `!cc` — change your piece symbol (up to twice)
- `!hi` — does nothing useful, just a greeting

## What's missing

Kings here only move one square, not the unlimited range they have in standard checkers. I skipped that to keep the move logic simpler — the AI inherits this simplification too, since it shares the same move-generation code. The AI also doesn't have an opening book or any positional heuristics beyond material count, so its early game is fairly generic; it gets noticeably sharper once captures start happening.

If you find a bug, open an issue.

## Running the tests

```
pip install -r requirements-dev.txt
pytest tests/ -v
```

45 tests covering the game engine and the AI's move generation/search. Runs automatically on every push via GitHub Actions.

## License

MIT
