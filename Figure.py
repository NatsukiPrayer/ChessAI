from abc import ABC
import pygame


class Figure(ABC):
    def __init__(
        self, power: int, position: list[int], color: bool, imgSize: int, image: str
    ) -> None:
        self.power = power
        self.position = position
        self.alive = True
        self.possibleMoves = []
        self.color = color
        self.image = pygame.image.load(image)
        self.imageRect = self.image.get_rect()
        self.motion = False

    def calculatePossibleMoves(self):
        pass

    def move(self, position: list[int]) -> None:
        if position not in self.possibleMoves:
            raise Exception("Cannot move")
        else:
            self.position = position

    def imgRect(self):
        self.imageRect = self.image.get_rect()
