from Figure import Figure
from Field import Field


class King(Figure):
    def __init__(self, power, position, color, imgSize, image):
        super(King, self).__init__(power, position, color, imgSize, image)

    def calculatePossibleMoves(self, field: Field) -> None:
        directions = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, 1),
            (1, -1),
            (-1, -1),
        ]
        for idx, direction in enumerate(directions):
            x = self.position[0] + direction[0]
            y = self.position[1] + direction[1]
            try:
                field.checkCell(x, y, self)
            except IndexError:
                pass
