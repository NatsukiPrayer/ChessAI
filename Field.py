from copy import copy
from typing import List, Optional, Tuple, Union, TYPE_CHECKING
import numpy as np
from Player import Player
from AIPlayer import AI
from random import randint
from pgn_parser import parser, pgn
import torch

if TYPE_CHECKING:
    from Figure import Figure


class Field:
    def __init__(self, players: Tuple[AI, AI], firstColor: bool):
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
        # players = (copy(players[0]), copy(players[1]))
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

    def train(self):
        Polyana = self
        while True:
            activePlayer = Polyana.players[int(self.turn)]
            nonActivePlayer = Polyana.players[int(not self.turn)]
            state_old_activePlayer = Polyana.calculatePowerOnDesk(activePlayer.color)
            state_old_activePlayer = torch.tensor(state_old_activePlayer).float()
            state_old_activePlayer = torch.unsqueeze(state_old_activePlayer, 0)
            action = activePlayer.net.forward(state_old_activePlayer)
            firstLine, piece, pos = activePlayer.getMove(action)
            action = torch.tensor(
                [
                    [
                        [
                            3 if cell != None and cell.position == piece.position else 0
                            for cell in row
                        ]
                        for row in self.cells
                    ],
                    [
                        [
                            3 if cell != None and cell.position == pos else 0
                            for cell in row
                        ]
                        for row in self.cells
                    ],
                ]
            ).float()
            action = torch.unsqueeze(action, 0)
            done, movingReward, newState = Polyana.makeMove(
                pos, piece, firstLine
            )  # type: ignore
            newState = torch.tensor(newState)
            activePlayer.remember(state_old_activePlayer, action, newState, done)
            activePlayer.train_short_memory(
                state_old_activePlayer, action, movingReward, newState, done
            )

            if self.draw:
                activePlayer.n_games += 1
                nonActivePlayer.n_games += 1
                self.players[0].changeScore(0.5)
                self.players[1].changeScore(0.5)
                return
            elif self.end:
                self.word = "white" if self.turn else "black"
                activePlayer.n_games += 1
                nonActivePlayer.n_games += 1
                self.players[int(not self.turn)].changeScore(1)
                return

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

    def makeMove(self, position, movedFigure, firstLine=False):
        movingReward = 0
        newState = self.calculatePowerOnDesk(movedFigure.color)
        if movedFigure is None:
            return
        pos = position
        if -1 < pos[0] < 8 and -1 < pos[1] < 8:
            if list(pos) != list(movedFigure.position):
                lastPos = movedFigure.position
                reward = movedFigure.move(pos)
                movingReward += reward
                newState = self.calculatePowerOnDesk(movedFigure.color)
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
            done = False
            if self.draw:
                movingReward += -15
                done = True
            if self.end:
                movingReward += 60
                done = True

            # print(self)
            return (done, movingReward, newState)

    def calculatePowerOnDesk(self, color: bool) -> np.ndarray:
        allMatrix = []
        for power in range(1, 7):
            matrix = []
            for row in self.cells:
                temp = []
                for cell in row:
                    if cell is None:
                        temp.append(0)
                    elif cell.power == power:
                        if cell.color == color:
                            temp.append(cell.power)
                        else:
                            temp.append(-cell.power)
                    else:
                        temp.append(0)
                matrix.append(temp)
            soqa = np.array(matrix)
            allMatrix.append(soqa)
        kavo = np.stack(allMatrix)
        return kavo


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
