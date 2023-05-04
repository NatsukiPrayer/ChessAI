from typing import List, Union
import numpy as np
from Figure import Figure


class Field:
    def __init__(self):
        self.cells: List[List[Figure | None]] = [
            [None for i in range(8)] for _ in range(8)
        ]
        notes = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.notes = {i: notes[i] for i in range(8)}

    def __getitem__(self, y: int) -> List[Figure | None]:
        return self.cells[y]

    def checkCell(self, x: int, y: int, fig: Figure) -> None:
        try:
            if self[x][y] == None or self[x][y].color != fig.color:  # type: ignore
                fig.possibleMoves.append((x, y))
        except IndexError:
            raise
