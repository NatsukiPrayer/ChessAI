from typing import TYPE_CHECKING
from Figure import Figure

if TYPE_CHECKING:
    from Field import Field


class Knight(Figure):
    def __init__(self, power, position, color, field):
        super(Knight, self).__init__(
            power,
            position,
            color,
            f"C:\\ChessIMG\\Knight{'W' if color else 'B'}.png",
            field,
        )
        self.letter = "N" if self.color else "n"

    def _thisFigureMoves(self, field: "Field") -> None:
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
