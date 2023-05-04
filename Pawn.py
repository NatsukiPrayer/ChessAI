from Figure import Figure
from Field import Field


class Pawn(Figure):
    def __init__(self, power, position, color, imgSize, image):
        super(Pawn, self).__init__(power, position, color, imgSize, image)

    def calculatePossibleMoves(self, field: Field) -> None:
        x, y = self.position
        direction = 1 if self.color else -1
        if (self.color and self.position[1] == 1) or (
            not self.color and self.position[1] == 6
        ):
            field.checkCell(x, y + 2 * direction, self)

        try:
            if field[x + 1][y + direction].color != self.color:  # type: ignore
                self.possibleMoves.append([x + 1, y + direction])
        except IndexError:
            pass
        except AttributeError:
            pass

        try:
            if field[x - 1][y + direction].color != self.color:  # type: ignore
                self.possibleMoves.append([x - 1, y + direction])
        except IndexError:
            pass
        except AttributeError:
            pass

        try:
            if field[x][y + direction] == None:
                self.possibleMoves.append([x, y + direction])
        except IndexError:
            pass
