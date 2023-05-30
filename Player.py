from typing import Any, Tuple, TYPE_CHECKING
from Pawn import Pawn
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from King import King

if TYPE_CHECKING:
    from Field import Field
    from Figure import Figure


class Player:
    color: bool
    field: "Field"

    def __init__(self, ID: int = -1):
        self.lastMove: Tuple["Figure" | None, int | None] = (None, None)
        self.ID = ID

    def gameInitialiaze(self, color: bool, field: "Field"):
        self.color = color
        self.field = field
        pawnRow = 1 if self.color else 6
        otherRow = 0 if self.color else 7

        pawns = [
            Pawn(
                1,
                (i, pawnRow),
                self.color,
                self.field,
            )
            for i in range(8)
        ]
        pieces = [
            Rook(
                4,
                (0, otherRow),
                self.color,
                self.field,
            ),
            Rook(
                4,
                (7, otherRow),
                self.color,
                self.field,
            ),
            Knight(
                2,
                (1, otherRow),
                self.color,
                self.field,
            ),
            Knight(
                2,
                (6, otherRow),
                self.color,
                self.field,
            ),
            Bishop(
                3,
                (2, otherRow),
                self.color,
                self.field,
            ),
            Bishop(
                3,
                (5, otherRow),
                self.color,
                self.field,
            ),
            Queen(
                5,
                (4, otherRow),
                self.color,
                self.field,
            ),
            King(
                6,
                (3, otherRow),
                self.color,
                self.field,
            ),
        ]
        self.pieces = [*pawns, *pieces]
        self.king = self.pieces[-1]

    def promote(self, promPiece: Pawn, promotion: int):
        proms = [
            "Queen",
            "Rook",
            "Knight",
            "Bishop",
        ]
        strPromotion = proms[promotion]
        x, y = promPiece.position
        self.pieces.pop(
            *[
                idx
                for idx, piece in enumerate(self.pieces)
                if piece.position == promPiece.position
            ]
        )
        del promPiece
        if strPromotion == "Queen":
            newPiece = Queen(
                6,
                (x, y),
                self.color,
                self.field,
            )
        elif strPromotion == "Rook":
            newPiece = Rook(
                4,
                (x, y),
                self.color,
                self.field,
            )
        elif strPromotion == "Knight":
            newPiece = Knight(
                2,
                (x, y),
                self.color,
                self.field,
            )
        elif strPromotion == "Bishop":
            newPiece = Bishop(
                3,
                (x, y),
                self.color,
                self.field,
            )
        else:
            raise ValueError("Invalid promotion")

        self.pieces.append(newPiece)
        self.field[x][y] = newPiece

    def checkFigDraw(self) -> bool:
        d = {}
        for piece in self.pieces:
            if piece not in d:
                d[str(piece)] = 0
            d[str(piece)] += 1
            if "P" in d or "p" in d:
                return False
            if "R" in d or "r" in d:
                return False
            if "Q" in d or "q" in d:
                return False
            if ("N" in d and d["N"] > 1) or ("n" in d and d["n"] > 1):
                return False
            if ("B" in d and d["B"] > 1) or ("b" in d and d["b"] > 1):
                return False
            if ("B" in d and d["B"] == 1) or ("b" in d and d["b"] == 1):
                if ("N" in d and d["N"] == 1) or ("n" in d and d["n"] == 1):
                    return False
        return True

    # def move(self, pickedPiece: Figure, pos: Tuple[int, int]) -> None:
    #     if any([piece.isUnderAttack for piece in self.pieces if piece != None]) and any(
    #         [piece.power == 6 for piece in self.pieces if piece != None]
    #     ):
    #         if pickedPiece.power == 6:
    #             pickedPiece.move(pos)
    #     else:
    #         pickedPiece.move(pos)
