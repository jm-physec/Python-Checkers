# Python-checkers

Checkers game for two players in the terminal. I made this as a programming exercise — it's pretty bare bones but fully playable.

No external libraries, just Python 3.

## Running it

```
python checkers.py
```

That's it.

## How it works

Board is 8x8, pieces only move on dark squares. White goes first.

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

White is `w`, black is `b`. When a piece gets crowned it turns uppercase (`W` or `B`).

You type moves as row + column, like `6A` to select a piece and `5B` to move it there.

Captures are mandatory, if you can take a piece you have to. Multijumps work too, the game will keep asking for destinations as long as the same piece can keep capturing.

Kings can move in all four diagonal directions (one square at a time, I kept it simple, maybe I will modify that in v2 if it comes).

## Commands

Type these at any point instead of a cell:

- `!end` — quit
- `!changename` or `!cn` — change your name (max 2 times per game)
- `!changechar` or `!cc` — change your piece symbol (max 2 times)
- `!hi` — easter egg :)

## What I might add later

- AI opponent (minimax probably, but that's a bigger project)
- Multi-jump is already in, but mandatory multi-capture chains could be stricter
- Maybe colors in the terminal? Looked complicated for now.
- Modify Kings moves to be like the classic game (all squares you want, not only one like now)

## Requirements

Just Python 3.8+, nothing to install.
