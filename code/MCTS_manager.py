import numpy as np
from game_nim import GameNim
from agent_MCT import AgentMCT
from ANET import ANET

class MctsManager:
    def __init__(self, game=GameNim, MCT=AgentMCT, ANET=ANET):
        self.game = game
        self.MCT = MCT
        self.ANET = ANET
    
    def trainANET(self, gameVariables, n_actualGames, n_searchGames, c, saveInterval):
        RBUF = np.array([])
        ANET = self.ANET()
        for i in range(n_actualGames):
            game = self.game(gameVariables)
            MCT = self.MCT(ANET, game.getBoardState(), 1, game, n_searchGames, c)
            while game.PlayerHasWon() == 0:
                for j in range(n_searchGames):
                    leaf = MCT.findLeaf()
                    node, playerHasWon = MCT.expandNode(leaf)
                    MCT.backpropagate(node, playerHasWon)
                D = MCT.getD()
                """ Should this really save just the root.boardstate?
                Should it also save player? """
                RBUF = np.append(RBUF, (MCT.root.boardState, D))
                # Return the move in D with most visitCOunts
                highestVisitMove = max(D, key=lambda x: x[1])
                game.update(highestVisitMove)
                # Set MCT.root to the new boardState and discard the other children nodes
                MCT.root = MCT.root.children[np.where(MCT.root.children.parentMove == highestVisitMove)]
                # Q: Are the other nodes discarded?
            """ Todo: Write these 2 lines
            and the method in ANET"""
            #randomSample = RBUF.....
            #ANET.train(randomSample)
            if i % saveInterval == 0:
                """ Todo: Write this method saving
                the parameters with name i"""
                ANET.saveParameters(i)