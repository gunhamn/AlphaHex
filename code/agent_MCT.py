import numpy as np
from ANET import ANET
from MCT_node import MctNode
from game_nim import GameNim

class AgentMCT:
    def __init__(self, ANET, boardState, playerNum, game=GameNim, n_simulations=100, c=1.4):
        self.ANET = ANET
        self.boardState = boardState
        self.playerNum = playerNum
        self.game = game
        self.rolloutGame = game
        self.n_simulations = n_simulations
        self.root = MctNode(boardState, playerNum, game.getLegalMoves(boardState, playerNum))
        self.c = c
    
    def findLeaf(self):
        """
        Question:
        Should the algorithm always explore a leaf node
        whenever there is a leaf node among the children?
        Or should it only do this the first time,
        from the root node?

        Question:
        How does the algorithm deal with finding
        a node that is a final state of the game?

        Question:
        Should the legal moves be stored in the node
        or explored every time?
        """
        node = self.root
        while node.visitCount > 0:
            node = max(node.children, key=lambda x: x.UCB(self.c))
            """ Question:
            Will this cause a bug when 2 childen has ucb == np.inf?"""
        return node

    def expandNode(self, node):
        """
        Question:
        How does the algorithm search the children
        in a way that connects legal moves to nodes
        and already existing children?
        """
        while node.playerHasWon == 0:
            self.rolloutGame.setBoardState(node.boardState, node.playerNum)
            # Implement ANET to make this line work
            move = max(node.untriedMoves, key=lambda x: self.ANET.predict(node.boardState, x))
            boardState, playerTurn, legalMoves, playerHasWon = self.rolloutGame.update(move)
            childNode = MctNode(boardState, playerTurn, legalMoves, node, move, playerHasWon)
            node.addChild(childNode) # This also remoce the move from untried moves
            node = childNode
        return node, playerHasWon

    def backpropagate(self, node, playerHasWon):
        while node is not None:
            node.visitCount += 1
            if node.playerNum == playerHasWon:
                node.winCount += 1
            node = node.parent

    def getD(self):
        """
        How to represent D?
        Here it is a list of tuples.
        """
        #  D = distribution of visit counts in MCT along all arcs emanating from root
        D = []
        for child in self.root.children:
            D.append(([child.move], child.visitCount))
        return (self.root, D)