import numpy as np

class MctNode:
    def __init__(self, boardState, playerNum, legalMoves, parent=None):
        self.boardState = boardState
        self.playerNum = playerNum
        self.parent = parent
        self.children = np.array([])
        self.winCount = 0
        self.visitCount = 0
    
    def ucb(self, c):
        pass
        #if self.visitCount == 0:
        #    return np.inf
        #else:
        #    return self.winCount / self.visitCount + c * np.sqrt(np.log(self.parent.visitCount) / self.visitCount)
