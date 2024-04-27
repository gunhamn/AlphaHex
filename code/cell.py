#cell for point in hex grid, makes it easier for computation of final state
class Cell:
    def __init__(self, position: str, value: int = 0):
        self.value = value
        self.neigbors = []
        self.pos = position
        self.checkNeigh = []

    def __str__(self):
        return f"{self.value}"
        