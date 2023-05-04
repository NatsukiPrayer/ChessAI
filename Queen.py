from Figure import Figure
from Field import Field


class Queen(Figure):
    def __init__(self, power, position, color, imgSize, image):
        super(Queen, self).__init__(power, position, color, imgSize, image)

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
        for i in range(1, 8):
            for idx, direction in enumerate(directions):
                x = self.position[0] + direction[0] * i
                y = self.position[1] + direction[1] * i
                try:
                    field.checkCell(x, y, self)
                    if field[x][y] != None:
                        directions.pop(idx)
                except IndexError:
                    directions.pop(idx)
