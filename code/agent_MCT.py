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
        self.root = MctNode(boardState, playerNum)
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
        while len(node.children) > 0:
            self.rolloutGame.setBoardState(node.boardState, node.playerNum)
            legalMoves = self.rolloutGame.getMoves()
            if len(legalMoves) > len(node.children):
                return legalMoves[len(node.children)]
            else:
                node = max(node.children, key=lambda x: x.ucb(self.c))
        return node

    def expandNode(self, node):
        """
        Question:
        How does the algorithm search the children
        in a way that connects legas moves to nodes
        and already existing children?
        """
        pass
        
        while len(node.legalMoves) > 0:
            node = max()
        # result = ...
        #backpropagate(self, node, result)


    def backpropagate(self, node, result):
        pass