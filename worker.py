import signal
from random import randint
from Field import Field
from Game import Game
from AIPlayer import AI
from typing import TYPE_CHECKING, Tuple
from time import sleep

if TYPE_CHECKING:
    from Player import Player

_parallSemaphore = None


def initialize(parallSemaphore):
    global _parallSemaphore
    _parallSemaphore = parallSemaphore
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def execute(players: Tuple[AI, AI], color):
    Andrey = Field(players, color)
    with _parallSemaphore:  # type: ignore
        Andrey.train()
    return players


def mainFunc(field):
    end = False
    draw = False
    word = "BLYAT"
    while True:
        while True:
            Fig = field.chooseFig(
                randint(0, len(field.players[int(field.turn)].pieces) - 1)
            )
            if not Fig is None:
                field.makeMove(
                    Fig.possibleMoves[randint(0, len(Fig.possibleMoves) - 1)], Fig
                )
                break
        # 5sleep(0.2)
        draw = field.draw
        end = field.end
        if end:
            word = field.loser
            print(f"{word} lost")
            return f"{word} lost"
        if draw:
            print(f"draw")
            return f"draw"
