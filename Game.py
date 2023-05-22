import sys
from typing import Tuple
import pygame
from Field import Field
from Constants import *
from copy import copy
from time import sleep
from random import randint
import multiprocessing as mp
from Player import Player


class Game:
    def __init__(self, players: Tuple[Player, Player], color: bool):
        self.game = pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clcok = pygame.time.Clock()
        self.screen.fill(BROWN)
        self.field = Field(players, color)
        self.showPossibleMoves = False
        self.blockSize = 125
        self.turn = True
        self.dictStates = {}
        self.end = False
        self.draw = False
        self.word = "BLYAT"
        self.font = pygame.font.SysFont("Arial", 70)
        self.isPromoting = False
        self.promotionPics = []
        self.movedFigure = None
        self.id = id
        self.redraw()
        # self.main()

    def redraw(self):
        self.screen.fill(BROWN)
        if self.movedFigure != None:
            self.movedFigure.calculatePossibleMoves(self.field)

        self.drawGrid()
        for piece in [p for pl in self.field.players for p in pl.pieces]:
            piece.imageRect.x = piece.position[0] * self.blockSize
            piece.imageRect.y = piece.position[1] * self.blockSize - (
                piece.image_offset if piece == self.movedFigure else 0
            )
            # if piece != self.field[piece.position[0]][piece.position[1]]:
            #     raise Exception()
            self.screen.blit(piece.image, piece.imageRect)
            if self.showPossibleMoves:
                self.drawPossibleMoves()
            if self.isPromoting:
                self.drawPromotions()
        pygame.display.flip()

    def drawPromotions(self):
        lastMove = self.field.players[not self.turn].lastMove
        if lastMove[0] != None:
            pos = lastMove[0].position
            Qimage = pygame.image.load(
                f"C:\\ChessIMG\\Queen{'W' if lastMove[0].color else 'B'}.png"
            )
            Kimage = pygame.image.load(
                f"C:\\ChessIMG\\Knight{'W' if lastMove[0].color else 'B'}.png"
            )
            Bimage = pygame.image.load(
                f"C:\\ChessIMG\\Bishop{'W' if lastMove[0].color else 'B'}.png"
            )
            Rimage = pygame.image.load(
                f"C:\\ChessIMG\\Rook{'W' if lastMove[0].color else 'B'}.png"
            )

            QimageRect = Qimage.get_rect()
            KimageRect = Kimage.get_rect()
            BimageRect = Bimage.get_rect()
            RimageRect = Rimage.get_rect()
            direction = -1 if lastMove[0].color else 1
            for enum, img in zip(
                enumerate([QimageRect, KimageRect, BimageRect, RimageRect]),
                [Qimage, Kimage, Bimage, Rimage],
            ):
                idx = enum[0]
                imgRect = enum[1]
                x, y = pos
                y = (y + direction * (idx + 1)) * self.blockSize
                x = x * self.blockSize
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, (200, 0, 255), rect, 0)
                self.screen.blit(img, rect)

        # my_image = pygame.Surface((self.blockSize, self.blockSize), pygame.SRCALPHA)
        # my_image.fill(GREEN_TRANSPARENT)
        # self.screen.blit(my_image, (x, y))

    def main(self):
        while True:
            while True:
                Fig = self.field.chooseFig(
                    randint(0, len(self.field.players[int(self.field.turn)].pieces) - 1)
                )
                if not Fig is None:
                    self.field.makeMove(
                        Fig.possibleMoves[randint(0, len(Fig.possibleMoves) - 1)], Fig
                    )
                    break
            # sleep(0.2)
            self.draw = self.field.draw
            self.end = self.field.end
            self.redraw()
            if self.end:
                rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
                pygame.draw.rect(self.screen, (255, 0, 0), rect, 0)
                self.word = "white" if self.field.turn else "black"
                self.screen.blit(
                    self.font.render(f"{self.word} LOSE", True, (0, 0, 0)), (200, 100)
                )
                pygame.display.flip()
                # print(self.field)
                # print()
                return [
                    f"{self.word} lost",
                    [self.field.players[i].ID for i in range(2)],
                ]
            if self.draw:
                rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 0)
                self.word = "Draw"
                self.screen.blit(
                    self.font.render(f"BOTHs LOSE", True, (0, 0, 0)), (200, 100)
                )
                pygame.display.flip()
                return [f"draw", [self.field.players[i].ID for i in range(2)]]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.isPromoting:
                        pass
                    else:
                        # Set the x, y postions of the mouse click
                        x, y = list(map(lambda x: x // self.blockSize, event.pos))
                        try:
                            figure = self.field.cells[x][y]
                            if figure.color != self.turn:
                                continue
                            figure.motion = True
                            self.movedFigure = figure
                            self.movedFigure.image_offset = 20
                            self.showPossibleMoves = True
                        except IndexError:
                            pass
                        except AttributeError:
                            pass
                        self.redraw()

                elif (
                    event.type == pygame.MOUSEMOTION
                    and self.movedFigure != None
                    and self.movedFigure.motion
                ):
                    pass
                elif (
                    event.type == pygame.MOUSEBUTTONUP
                    and self.movedFigure != None
                    and self.movedFigure.motion
                ):
                    pos = tuple(map(lambda x: x // self.blockSize, event.pos))
                    self.field.makeMove(pos, self.movedFigure)

                    self.showPossibleMoves = False
                    self.draw = self.field.draw
                    self.end = self.field.end
                    self.turn = self.field.turn
                    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    # print(self.field)
                    self.redraw()

    def drawGrid(self):
        for x in range(0, WINDOW_WIDTH, self.blockSize):
            for y in range(0, WINDOW_HEIGHT, self.blockSize):
                if (x + y) % (2 * self.blockSize) == 0:
                    rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                    pygame.draw.rect(self.screen, GREY, rect, 0)

    def drawPossibleMoves(self):
        if self.movedFigure == None:
            return
        # print(self.movedFigure.possibleMoves)
        for move in self.movedFigure.possibleMoves:
            x = (2 * move[0]) * self.blockSize // 2
            y = (2 * move[1]) * self.blockSize // 2
            my_image = pygame.Surface((self.blockSize, self.blockSize), pygame.SRCALPHA)
            my_image.fill(GREEN_TRANSPARENT)
            self.screen.blit(my_image, (x, y))

    def __del__(self) -> None:
        pass

    # Andrey.main()  # type: ignore
