from typing import TYPE_CHECKING, Tuple
from Figure import Figure
from random import randint

if TYPE_CHECKING:
    from Field import Field


class Pawn(Figure):
    def __init__(self, power, position, color, field):
        super(Pawn, self).__init__(
            power,
            position,
            color,
            f"C:\\ChessIMG\\Pawn{'W' if color else 'B'}.png",
            field,
        )
        self.letter = "P" if self.color else "p"

    def _thisFigureMoves(self, field: "Field") -> None:
        x, y = self.position
        direction = 1 if self.color else -1
        if (self.color and y == 1) or (not self.color and y == 6):
            if field[x][y + 2 * direction] == None:
                self.forwardMoves.append((x, y + 2 * direction))

        try:
            if field[x + 1][y + direction].color != self.color:  # type: ignore
                self.possibleMoves.append((x + 1, y + direction))

        except IndexError:
            pass
        except AttributeError:
            pass

        try:
            lastMove = self.field.players[int(not self.color)].lastMove
            if isinstance(lastMove[0], Pawn) and lastMove[1] == 2:
                if (
                    self.position[0] + 1 == lastMove[0].position[0]
                    and abs(self.position[1] - lastMove[0].position[1]) == 0
                ):
                    self.possibleMoves.append((x + 1, y + direction))
                elif (
                    self.position[0] - 1 == lastMove[0].position[0]
                    and abs(self.position[1] - lastMove[0].position[1]) == 0
                ):
                    self.possibleMoves.append((x - 1, y + direction))
        except IndexError:
            pass

        try:
            if field[x - 1][y + direction].color != self.color:  # type: ignore
                self.possibleMoves.append((x - 1, y + direction))
        except IndexError:
            pass
        except AttributeError:
            pass

        try:
            if field[x][y + direction] == None:
                self.forwardMoves.append((x, y + direction))
        except IndexError:
            pass

    def move(self, position: Tuple[int, int]) -> bool:
        super().move(position)
        self.movesWithoutUnchangeableChanges = 0
        if self.position[1] in (0, 7):
            self.field.players[int(self.color)].promote(self, randint(0, 3))  # type: ignore
            self = None
            return True
        return False
