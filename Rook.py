from typing import TYPE_CHECKING
from Figure import Figure

if TYPE_CHECKING:
    from Field import Field


class Rook(Figure):
    def __init__(self, power, position, color, field):
        super(Rook, self).__init__(
            power,
            position,
            color,
            f"C:\\ChessIMG\\Rook{'W' if color else 'B'}.png",
            field,
        )
        self.letter = "R" if self.color else "r"

    def _thisFigureMoves(self, field: "Field") -> None:
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for i in range(1, 8):
            for idx, direction in enumerate(directions):
                if direction != (10, 10):
                    x = self.position[0] + direction[0] * i
                    y = self.position[1] + direction[1] * i
                    try:
                        field.checkCell(x, y, self)

                        if field[x][y] != None:
                            directions[idx] = (10, 10)
                    except IndexError:
                        # directions.pop(idx)
                        pass
