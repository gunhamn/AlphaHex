from ANET import ANET
from game_nim import GameNim
from MCT import mct
import numpy as np
from agent_human import AgentHuman
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
            while self.game.isFinalState(self.state[0], self.state[1]) == None:
                print('ITS IN WHILE')
                for sim in range(number_sim):
                    self.tree.sim()
                D = self.tree.distribution()
                RBUF = RBUF.append([[self.tree.root.boardState, self.tree.root.player], D])
                action = np.argmax(D)
                self.state = self.game.actionOnState(action, self.state[0], self.state[1])
                self.tree.root = self.tree.root.children[action]
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
                action = np.argmax(network.forward(state))
                game.update(moves[action], verbose=verbose)
            else:
                move = agent.makeMove(game, moves)
                game.update(move, verbose=verbose)
        if verbose:
            print(f"Player {game.PlayerHasWon()} won!")
        return game.PlayerHasWon()
    
def main():
    game = GameNim()
    system = rl_system(game)
    net = system.train(2, 10, 100)
    winner = playGame(game, net)



main()