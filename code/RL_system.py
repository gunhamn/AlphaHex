from ANET import ANET
from game_nim import GameNim
from MCT import mct
import numpy as np
from agent_human import AgentHuman
import torch
class rl_system:
    #def __init__(self, net:ANET, tree: mct, game: GameNim) -> None:
    def __init__(self, game: GameNim) -> None:
        self.net = None
        self.tree = None
        self.game = game
        self.state = None
        pass

    def train(self, saveI, number_games, number_sim):
        #RBUF = np.array([]) #this is sketchy, just use list?
        RBUF = []
        self.net= ANET(numInput=2, numOutput=2)
        for game in range(number_games):
            self.game.reset()
            self.state=[0,0]
            self.state[0], self.state[1] = self.game.getBoardState()
            s_init = [0,0]
            s_init[0], s_init[1] = self.game.getBoardState()
            self.tree = mct(state=s_init, game = self.game, network=self.net)
            print(f"tree root before while: {self.tree.root.boardState}")
            while self.game.isFinalState(self.state[0], self.state[1]) == None:
                print('ITS IN WHILE')
                for sim in range(number_sim):
                    self.tree.sim()
                print(f'sim is done for {game}')
                D = self.tree.distribution()
                print(f'Distribution : {D}')
                print(f"RBUF: {RBUF}")
                RBUF.append([[self.tree.root.boardState[0], self.tree.root.player], D])
                action = np.argmax(D)
                print(f"IT GETS HERE")
                self.state = self.game.actionOnState(action, self.state[0], self.state[1])
                self.tree.root = self.tree.root.children[action] #not here 
            self.net.train(RBUF)
            if game % saveI == 0:
                #save ANET for tournament play
                pass
        return self.net

def playGame(game: GameNim, network: ANET, verbose=True):
        agent = AgentHuman(2)
        while game.PlayerHasWon() == 0:
            if verbose:
                game.printGameState()
            moves = game.getMoves()
            state=[0,0]
            state[0], state[1] = game.getBoardState()
            if game.playerTurn == 1:
                netState= [state[0][0], state[1]]
                print(f"state: {network.forward(netState)}")
                action = torch.argmax(network.forward(netState))
                game.update(moves[action], verbose=verbose)
            else:
                move = agent.makeMove(game, moves)
                game.update(move, verbose=verbose)
        if verbose:
            print(f"Player {game.PlayerHasWon()} won!")
        return game.PlayerHasWon()
    
def main():
    print("RUN BEGINS")
    game = GameNim(gameVariables=[5,2])
    system = rl_system(game)
    net = system.train(2, 10, 3)
    testgame = GameNim(gameVariables=[5,2])
    winner = playGame(testgame, net)



main()