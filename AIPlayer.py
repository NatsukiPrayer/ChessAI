import os
from Player import Player
from typing import TYPE_CHECKING, Any
import torch
import torch.utils.data
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import torch.optim as optim
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King
from collections import deque
from Trainer import QTrainer
import random

if TYPE_CHECKING:
    from Field import Field


class module(nn.Module):
    def __init__(self, hidden_size):
        super(module, self).__init__()
        self.conv1 = nn.Conv2d(hidden_size, hidden_size, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(hidden_size, hidden_size, 3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(hidden_size)
        self.bn2 = nn.BatchNorm2d(hidden_size)
        self.activation1 = nn.SELU()
        self.activation2 = nn.SELU()

    def forward(self, x):
        x_input = torch.clone(x)
        x = self.conv1(x)
        x = self.bn1(x)

        x = self.activation1(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = x + x_input
        x = self.activation2(x)
        return x


class ChessNet(nn.Module):
    def __init__(self, hidden_layers=4, hidden_size=200):
        super(ChessNet, self).__init__()
        self.hidden_layers = hidden_layers
        self.input_layer = nn.Conv2d(6, hidden_size, 3, stride=1, padding=1)
        self.module_list = nn.ModuleList(
            [module(hidden_size) for _ in range(hidden_layers)]
        )
        self.output_layer = nn.Conv2d(hidden_size, 2, 3, stride=1, padding=1)

        # # Input layers
        # self.fc1 = nn.Linear(64, 256)
        # self.fc2 = nn.Linear(256, 128)

        # # Piece type layers
        # self.fc_type1 = nn.Linear(128, 64)
        # self.fc_type2 = nn.Linear(64, 6)  # 6 represents the number of piece types

        # # Move layers
        # self.fc_move1 = nn.Linear(128, 64)

    def forward(self, x):
        x = self.input_layer(x)
        x = F.relu(x)
        for i in range(self.hidden_layers):
            x = self.module_list[i](x)
        x = self.output_layer(x)
        return x

    def longTrain(self, state, action, new_state, done):
        pass

    def shortTrain(self, state, action, new_state, done):
        pass

        # x = torch.Tensor(x).ravel()
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))

        # # Piece type prediction
        # type_output = F.relu(self.fc_type1(x))
        # type_output = self.fc_type2(type_output)
        # type_probs = F.softmax(
        #     type_output, dim=-1
        # )  # Apply softmax to get probabilities

        # # Move coordinates prediction
        # move_input = F.relu(self.fc_move1(x))
        # move_probs = F.softmax(move_input, dim=-1)  # Apply softmax to get probabilities

        # return type_probs, move_probs


LR = 0.0009
BATCH_SIZE = 100


class AI(Player):
    def __init__(self, ID: int, score: float = 0, memory=deque(maxlen=100)):
        super(AI, self).__init__(ID)
        # self.net = Net()
        self.score = score
        self.n_games = 0
        self.epsilon = 0
        self.memory = memory
        self.gamma = 0
        self.net = ChessNet()
        self.trainer = QTrainer(self.net, lr=LR, gamma=self.gamma)

    def __reduce__(self) -> str | tuple[Any, ...]:
        self.memory = deque(
            [
                (mem[0].detach(), mem[1].detach(), mem[2].detach(), mem[3])
                for mem in self.memory
            ],
            maxlen=100,
        )
        self.save()

        return (self.__class__, (self.ID, self.score, self.memory))

    def gameInitialiaze(self, color: bool, field: "Field"):
        super().gameInitialiaze(color, field)
        if os.path.exists(f"NNN/Player{self.ID}.pt"):
            self.load()

    def save(self):
        torch.save(self.net, f"NNN/Player{self.ID}.pt")

    def load(self):
        self.net = torch.load(f"NNN/Player{self.ID}.pt")

    def changeScore(self, change: float) -> None:
        self.score += change

    def remember(self, state, action, new_state, done):
        self.memory.append((state, action, new_state, done))

    def randomMove(self):
        piece = random.choice(self.pieces)
        piece.calculatePossibleMove()
        return (piece, random.choice(piece.possibleMoves))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def outputDecesion(self, board):
        output = []
        for rowidx, row in enumerate(board.tolist()):
            for cellidx, cell in enumerate(row):
                output.append(((rowidx, cellidx), cell))
        return sorted(output, key=lambda x: x[1], reverse=True)

    def getMove(self, output):
        moveFrom = self.outputDecesion(output[0][0])
        moveTo = self.outputDecesion(output[0][1])
        firstLine = True
        for move in moveFrom:
            x, y = move[0]
            if self.field[x][y] == None or self.field[x][y].color != self.color:
                continue
            fig = self.field.cells[x][y]
            fig.calculatePossibleMoves(self.field)
            for move2 in moveTo:
                if move2[0] in fig.possibleMoves:
                    return (firstLine, fig, move2[0])  # type: ignore

                firstLine = False

        raise Exception("How???")  # type: ignore


# def train():
#     Oleg = AI(0)
#     Natasha = AI(1)
#     Players = (Oleg, Natasha)
#     Polyana = Field(Players, False)

#     turn = True
#     while True:
#         activePlayer = Polyana.players[int(turn)]
#         nonActivePlayer = Polyana.players[(int(turn) + 1) % 2]
#         state_old_activePlayer = Polyana.calculatePowerOnDesk(activePlayer.color)
#         state_old_nonActivePlayer = state_old_activePlayer * -1
#         state_old_activePlayer = torch.tensor(state_old_activePlayer).float()
#         state_old_activePlayer = torch.unsqueeze(state_old_activePlayer, 0)
#         action = activePlayer.net.forward(state_old_activePlayer)
#         firstLine, piece, pos = activePlayer.getMove(action)
#         (done, movingReward, enemyReward, newState) = Polyana.makeMove(
#             pos, piece, firstLine
#         )  # type: ignore
#         state_new_nonActivePlayer = newState * -1
#         activePlayer.remember(state_old_activePlayer, action, newState, done)
#         nonActivePlayer.remember(
#             state_old_nonActivePlayer, action, state_new_nonActivePlayer, done
#         )
#         if done:
#             activePlayer.n_games += 1
#             nonActivePlayer.n_games += 1
#             break
#         turn = not turn
#     return Polyana


if __name__ == "__main__":
    from Field import Field
    import chess.pgn

    net = ChessNet()

    Players = (AI(1), AI(0))

    # batch_size = 32

    # train_dataset = torch.utils.data.TensorDataset(train_X, train_y)
    # train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    # pgn = open("C:\ChessAI\lichess_db_standard_rated_2013-01.pgn")
    # while True:
    #     game = chess.pgn.read_game(pgn)
    #     if game is None:
    #         break
    #     field = Field(Players, False)
    #     for idx, move in enumerate(game.mainline_moves()):
    #         state = field.calculatePowerOnDesk(Players[(idx + 1) % 2].color)
    #         output = net.forward(state)
    #         move = str(move)
    #         oldPos = 7 - ord(move[0]) + ord("a"), int(move[1]) - 1
    #         newPos = (7 - ord(move[2]) + ord("a"), int(move[3]) - 1)
    #         Fig = field.cells[oldPos[0]][oldPos[1]]
    #         if not Fig is None:
    #             correctOutput = (Fig.power, oldPos, newPos)
    #         field.makeMove(newPos, Fig)

    fld = Field(Players, False)
    print(torch.cuda.is_available())
    lst = [
        [4, 1, 0, 0, 0, 0, -1, -4],
        [2, 1, 0, 0, 0, 0, -1, -2],
        [3, 1, 0, 0, 0, 0, -1, -3],
        [6, 1, 0, 0, 0, 0, -1, -6],
        [5, 1, 0, 0, 0, 0, -1, -5],
        [3, 1, 0, 0, 0, 0, -1, -3],
        [2, 1, 0, 0, 0, 0, -1, -2],
        [4, 1, 0, 0, 0, 0, -1, -4],
    ]
    # lst = torch.Tensor(fld.calculatePowerOnDesk(False)).float()
    # lst = lst.unsqueeze(0)
    # res = net.forward(lst)
    # metricFrom = nn.CrossEntropyLoss()
    # metricTo = nn.CrossEntropyLoss()
    # # loss_from = metricFrom(res[:, 0, :], y[:, 0, :])
    # # loss_to = metricTo(res[:, 1, :], y[:, 1, :])
    # # loss = loss_from + loss_to

    # print(res)

    # torch.save(net, "setka")

    # for idx, x in sorted(
    #     list(enumerate(res[1].tolist())), key=lambda x: x[1], reverse=True
    # ):
    #     print(idx, x)

# polyana = train()
# print(polyana.players[0].pieces)
# print(polyana.players[1].pieces)
