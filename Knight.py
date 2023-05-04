from Figure import Figure
from Field import Field


class Knight(Figure):
    def __init__(self, power, position, color, imgSize, image):
        super(Knight, self).__init__(power, position, color, imgSize, image)

    def calculatePossibleMoves(self, field: Field) -> None:
        for x, y in (
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ):
            x += self.position[0]
            y += self.position[1]
            try:
                field.checkCell(x, y, self)
            except IndexError:
                pass
