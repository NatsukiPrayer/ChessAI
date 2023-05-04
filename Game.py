import sys
import pygame
from Field import Field
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King

BROWN = (101, 67, 33)
GREY = (115, 115, 115)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000

blackPawns = [Pawn(1, [6, i], False, 125, "C:\\ChessIMG\\PawnB.png") for i in range(8)]
whitePawns = [Pawn(1, [1, i], True, 125, "C:\\ChessIMG\\PawnW.png") for i in range(8)]


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BROWN)
    drawGrid(SCREEN)
    moving = False
    movedFigure = Pawn(1, [6, 1], False, 125, "C:\\ChessIMG\\PawnB.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                x, y = event.pos
                try:
                    figure = [
                        piece
                        for piece in blackPawns
                        if piece.imageRect.collidepoint(x, y)
                    ][0]
                    figure.motion = True
                    movedFigure = figure
                    print(f"clicked on image, it is {figure.color}")
                except IndexError:
                    pass
                try:
                    figure = [
                        piece
                        for piece in whitePawns
                        if piece.imageRect.collidepoint(x, y)
                    ][0]
                    figure.motion = True
                    movedFigure = figure
                    print(f"clicked on image, it is {figure.color}")
                except IndexError:
                    pass
            elif event.type == pygame.MOUSEMOTION:  # type: ignore
                movedFigure.imageRect.move_ip(event.rel)  # type: ignore

            elif event.type == pygame.MOUSEBUTTONUP and movedFigure.motion:  # type: ignore
                movedFigure.motion = False  # type: ignore
        pygame.display.update()


def drawGrid(screen):
    blockSize = 125  # Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            if (x + y) % (2 * blockSize) == 0:
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(SCREEN, GREY, rect, 0)
    for i in range(len(blackPawns)):
        blackPawns[i].imgRect()
        blackPawns[i].imageRect.center = (
            2 * i + 1
        ) * blockSize // 2, 3 * blockSize // 2
        screen.blit(blackPawns[i].image, blackPawns[i].imageRect)
        pygame.display.flip()
    for i in range(len(whitePawns)):
        whitePawns[i].imgRect()
        whitePawns[i].imageRect.center = (
            2 * i + 1
        ) * blockSize // 2, 13 * blockSize // 2
        screen.blit(whitePawns[i].image, whitePawns[i].imageRect)
        pygame.display.flip()


if __name__ == "__main__":
    main()
