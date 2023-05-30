from abc import ABC
from typing import Tuple, TYPE_CHECKING

import pygame
from random import randint

if TYPE_CHECKING:
    from Field import Field
    from Pawn import Pawn


class Figure(ABC):
    def __init__(
        self,
        power: int,
        position: Tuple[int, int],
        color: bool,
        image: str,
        field: "Field",
    ) -> None:
        self.field = field
        self.power = power
        self.position = position
        self.alive = True
        self.possibleMoves = []
        self.color = color
        self.image = pygame.image.load(image)
        self.imageRect = self.image.get_rect()
        self.motion = False
        self.image_offset = 0
        self.isUnderAttack = False
        self.forwardMoves = []
        self.h = power if color else -power
        self.field.set(self)
        self.field.hash ^= self.field.hashStates[position[0]][position[1]][self.h]
        self.letter = ""

    def calculatePossibleMoves(self, field: "Field", depth: int = 0):
        self.possibleMoves = []
        self.forwardMoves = []
        self._thisFigureMoves(field)

        if depth == 0:
            if self.power == 1:
                self.possibleMoves += self.forwardMoves
            x, y = self.position
            self.field[x][y] = None
            idx = 0
            while idx < len(self.possibleMoves):
                move = self.possibleMoves[idx]
                oldFig = self.field[move[0]][move[1]]
                self.field[move[0]][move[1]] = self
                for piece in self.field.players[int(not self.color)].pieces:
                    piece.calculatePossibleMoves(self.field, 1)
                    if self.field.players[int(self.color)].king != self:
                        if (
                            piece.position != move
                            and self.field.players[int(self.color)].king.position
                            in piece.possibleMoves
                        ):
                            self.possibleMoves.pop(idx)
                            idx -= 1
                            break
                    else:
                        if piece.position != move and move in piece.possibleMoves:
                            self.possibleMoves.pop(idx)
                            idx -= 1
                            break
                self.field.cells[move[0]][move[1]] = oldFig
                idx += 1
            self.field[x][y] = self

    def _thisFigureMoves(self, field: "Field"):
        pass

    def __delete__(self, instance):
        print("HEY!")

    def move(self, position: Tuple[int, int]) -> int:
        reward = 0
        if position not in self.possibleMoves:
            return reward
        reward += 1
        self.field.movesWithoutUnchangeableChanges += 1
        x, y = position
        old_x, old_y = self.position
        lastMove = self.field.players[int(not self.color)].lastMove
        takenFigure = self.field[x][y]
        if lastMove[0] != None:
            if lastMove[0].power == 1 and lastMove[1] == 2:
                if self.power == 1:
                    direction = 1 if self.color else -1
                    if lastMove[0].position[1] + direction == y:
                        takenFigure = lastMove[0]
                        self.field[lastMove[0].position[0]][
                            lastMove[0].position[1]
                        ] = None
        self.field[x][y] = self
        self.field[old_x][old_y] = None
        self.field.hash ^= self.field.hashStates[x][y][self.h]
        self.field.hash ^= self.field.hashStates[old_x][old_y][self.h]
        if takenFigure != None:
            self.field.movesWithoutUnchangeableChanges = 0
            self.field.hash ^= self.field.hashStates[x][y][takenFigure.h]

            self.field.players[int(takenFigure.color)].pieces.pop(
                *[
                    idx
                    for idx, piece in enumerate(
                        self.field.players[int(takenFigure.color)].pieces
                    )
                    if piece.position == takenFigure.position
                ]
            )
            del takenFigure
        self.field.players[int(self.color)].lastMove = (
            self,
            abs(position[1] - self.position[1]),
        )
        self.position = position
        for piece in self.field.players[int(self.color)].pieces:
            piece.calculatePossibleMoves(self.field)
            if (
                self.field.players[int(not self.color)].king.position
                in piece.possibleMoves
            ):
                reward = 5
                break
        return reward

    def __repr__(self) -> str:
        return self.letter
