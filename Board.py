import numpy as np

class Board:
    def __init__(self):
        self.field = np.array([[0 for i in range(8)] for _ in range(8)])


Andrei = Board()
print(Andrei.field)