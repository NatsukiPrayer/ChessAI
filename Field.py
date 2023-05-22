from copy import copy
from typing import List, Optional, Tuple, Union, TYPE_CHECKING
import numpy as np
from Player import Player
from random import randint

if TYPE_CHECKING:
    from Figure import Figure


class Field:
    def __init__(self, players: Tuple[Player, Player], firstColor: bool):
        self.cells: List[List["Figure" | None]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        # notes = ["A", "B", "C", "D", "E", "F", "G", "H"]
        # self.state = {i: notes[i] for i in range(8)}
        self.hashStates = [
            [[0] + [randint(1, 2**64 - 1) for i in range(12)] for j in range(8)]
            for k in range(8)
        ]
        self.movesWithoutUnchangeableChanges = 0
        self.hash = 0
        self.draw = False
        self.end = False
        self.turn = True
        self.loser = ""
        self.dictStates = {}
        players = (copy(players[0]), copy(players[1]))
        players[0].gameInitialiaze(firstColor, self)
        players[1].gameInitialiaze(not firstColor, self)
        self.players = players

    def __getitem__(self, y: int) -> List[Optional["Figure"]]:
        return self.cells[y]

    def set(self, f: "Figure") -> None:
        x, y = f.position
        self.cells[x][y] = f

    def __hash__(self) -> int:
        return self.hash

    def checkCell(self, x: int, y: int, fig: "Figure") -> None:
        try:
            if x < 0 or y < 0:
                raise IndexError("Outside bounds")
            if self[x][y] == None or self[x][y].color != fig.color:  # type: ignore
                fig.possibleMoves.append((x, y))

        except IndexError:
            raise

    def calculateAllPossibleMoves(self):
        for row in self.cells:
            for piece in row:
                if piece != None:
                    piece.calculatePossibleMoves(self)

    def __repr__(self) -> str:
        return "\n".join(
            "".join(map(lambda x: str(x) if x else "_", row)) for row in self
        )

    def chooseFig(self, indx: int) -> "Figure":
        pieces = self.players[int(self.turn)].pieces
        fig = pieces[indx]
        fig.calculatePossibleMoves(self)
        if len(fig.possibleMoves) > 0:
            return fig
        else:
            return None  # type: ignore

    def makeMove(self, position, movedFigure):
        if movedFigure is None:
            return
        pos = position
        if -1 < pos[0] < 8 and -1 < pos[1] < 8:
            if list(pos) != list(movedFigure.position):
                lastPos = movedFigure.position
                movedFigure.move(pos)
                if lastPos != movedFigure.position:
                    self.turn = not self.turn
                    if all([player.checkFigDraw() for player in self.players]):
                        self.draw = True
                    if self.movesWithoutUnchangeableChanges == 50:
                        self.draw = True
                    if hash(self) not in self.dictStates:
                        self.dictStates[hash(self)] = 1
                    else:
                        self.dictStates[hash(self)] += 1
                    if self.dictStates[hash(self)] == 3:
                        self.draw = True

                    for piece in self.players[int(self.turn)].pieces:
                        piece.calculatePossibleMoves(self)
                        if len(piece.possibleMoves) > 0:
                            break
                    else:
                        for piece in self.players[int(not self.turn)].pieces:
                            piece.calculatePossibleMoves(self)
                            if (
                                self.players[int(self.turn)].king.position
                                in piece.possibleMoves
                            ):
                                self.end = True
                                self.loser = "white" if self.turn else "black"
                                break
                        else:
                            self.draw = True

            movedFigure.image_offset = 0
            movedFigure.motion = False
            movedFigure = None

    def calculatePowerOnDesk(self, color: bool) -> list:
        matrix = []
        for row in self.cells:
            temp = []
            for cell in row:
                if cell is None:
                    temp.append(0)
                elif cell.color == color:
                    temp.append(cell.power)
                else:
                    temp.append(-cell.power)
            matrix.append(temp)
        return matrix


# class Field:
#     def __init__(self):
#         self.__observers = set()

#     # Подключить наблюдателя(клетку) к системе. (просто добавляем объект в список).
#     def attach(self, observer):
#         self.__observers.add(observer)

#     # Отключить наблюдателя(камеру) от системы. (просто удаляем объект из список).
#     def detach(self, observer):
#         self.__observers.remove(observer)

#     # Отправка уведомления\команды всем наблюдателям(камерам) подключенным к системе.
#     # (Проходимся по списку объектов и вызываем нужный метод).
#     def notify(self):
#         for observer in self.__observers:
#             observer.refresh()


# class Cell:
#     """Камера наблюдения."""

#     def __init__(self, name, pos):
#         self.name = name
#         self.figure = None
#         self.pos = pos

#     def move(self, cell: "Cell"):
#         cell.figure = self.figure
#         self.figure = None

#     def refresh(self):
#         pass
