# Shifumi

A very simple shifumi game, docker-friendly

## Server configuration

Listen by default on `tcp://0.0.0.0:22451`. The first player that reachs 5 wins wins the game.

Environnement variables `SHIFUMI_ADDRESS`, `SHIFUMI_PORT` and `SHIFUMI_GAMES` can be set to replace the default values.

## Spec

### Server -> Client

* `b"s"` starts the game
* `b"w"` wins, `b"d"` draws, `b"l"` looses
* `b"e"` ends the game

### Client -> Server

* `b"s"` plays scisor, `b"p"` plays paper, `b"r"` plays rock
* `b"e"` ends the game
