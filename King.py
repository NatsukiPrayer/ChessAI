from typing import TYPE_CHECKING
from Figure import Figure

if TYPE_CHECKING:
    from Field import Field


class King(Figure):
    def __init__(self, power, position, color, field):
        super(King, self).__init__(
            power,
            position,
            color,
            f"C:\\ChessIMG\\King{'W' if color else 'B'}.png",
            field,
        )
        self.letter = "K" if self.color else "k"

    def _thisFigureMoves(self, field: "Field") -> None:
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
