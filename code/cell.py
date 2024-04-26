#cell for point in hex grid, makes it easier for computation of final state
class Cell:
    def __init__(self, position: str):
        self.value = 0
        self.neigbors = []
        self.pos = position

    def __str__(self):
        return f"{self.value}"
        