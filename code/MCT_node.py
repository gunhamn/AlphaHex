import numpy as np

class MctNode:
    def __init__(self, boardState, playerNum, untriedMoves, parent=None, parentMove=None, playerHasWon=0):
        self.boardState = boardState
        self.playerNum = playerNum
        self.untriedMoves = untriedMoves
        self.parent = parent
        self.parentMove = parentMove
        self.children = np.array([])
        self.winCount = 0
        self.visitCount = 0
        self.playerHasWon = 0
    
    def UCB(self, c):
        if self.visitCount == 0:
            return np.inf
        else:
            return self.winCount / self.visitCount + c * np.sqrt(np.log(self.parent.visitCount) / self.visitCount)
    
    def addChild(self, node):
        self.children = np.append(self.children, node)
        self.untriedMoves.remove(node.parentMove)