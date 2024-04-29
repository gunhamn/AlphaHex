from ANET import ANET
from gameNim import GameNim
from MCT import mct
import numpy as np
from agent_human import AgentHuman
import torch
import os
class rl_system:
    def __init__(self, game: GameNim) -> None:
        self.net = None
        self.tree = None
        self.game = game
        self.state = None
        pass

    def train(self, saveI, number_games, number_sim, eps):
        RBUF = []
        self.net= ANET(numInput=2, numOutput=2)
        for game in range(number_games):
            print(f'its in new game {game}')
            self.game.reset(gameVariables=[5,2])
            self.state=[0,0]
            self.state[0], self.state[1] = self.game.getBoardState()
            self.tree = mct(state=self.state, game = self.game, network=self.net)
            while self.game.isFinalState(self.state[0], self.state[1]) == None: #Trenge ikke ta inn parametre
                for sim in range(number_sim):
                    self.tree.sim(eps=eps/(game+1))
                D = self.tree.distribution()
                RBUF.append([[self.tree.root.boardState[0], self.tree.root.player], D])
                action = np.argmax(D)
                self.state = self.game.actionOnState(action, self.state[0], self.state[1])
                self.tree.root = self.tree.root.children[action] #not here
            self.net.train(RBUF)
            if game % saveI == 0:
                #save ANET for tournament play
                torch.save(self.net, f"code/networks/network_{game}")
                pass
        with open('output.txt', 'w') as file:
            # Iterate over the list and write each element to the file
            for item in RBUF:
                file.write(f"{item}" + '\n') 
       # print(f"data: {RBUF}")
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
                netState= [state[0][0], 1]
                #print(f"state: {network.forward(netState, moves=moves)}")
                action = torch.argmax(network.forward(netState))
                game.update(moves[action], verbose=verbose)
            else:
                move = agent.makeMove(game, moves)
                game.update(move, verbose=verbose)
        if verbose:
            print(f"Player {game.PlayerHasWon()} won!")
        return game.PlayerHasWon()

def playGamesAI(numberGames: int, player1: ANET, player2: ANET, verbose=True):
        wincount = [0,0]
        for i in range(numberGames):
            game = GameNim(gameVariables=5)
            if i % 2 == 0:
                while game.isFinalState() == None:
                    if verbose:
                        game.printGameState()
                    state = game.getBoardState()
                    if state[0] == 1:
                        netState= [state[1], state[0]]
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = torch.argmax(player1.forward(netState))
                        game.update(action, verbose=verbose)
                    else:
                        netState= [state[1], state[0]]
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = torch.argmax(player2.forward(netState))
                        game.update(action, verbose=verbose)
                if verbose:
                    print(f"Player {game.isFinalState()} won!")
                if game.isFinalState ==1:
                    wincount[0]+=1
                else:
                    wincount[1]+=1
            else:
                while game.isFinalState() == None:
                    if verbose:
                        game.printGameState()
                    state = game.getBoardState()
                    if state[0] == 1:
                        netState= [state[1], state[0]]
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = torch.argmax(player2.forward(netState))
                        game.update(action, verbose=verbose)
                    else:
                        netState= [state[1], state[0]]
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = torch.argmax(player1.forward(netState))
                        game.update(action, verbose=verbose)
                if verbose:
                    print(f"Player {game.PlayerHasWon()} won!")
                if game.isFinalState ==1:
                    wincount[1]+=1
                else:
                    wincount[0]+=1
        return wincount

def testNetworks():
    #test all networks against eachother, tournament code 
    pass
    
def main():
    print("RUN BEGINS")
    """networks_dir = os.path.join(os.path.dirname(__file__), 'networks')
    print(networks_dir)"""
    
    """ game = GameNim(gameVariables=[5,2])
    system = rl_system(game)
    net = system.train(saveI=10, number_games=100, number_sim=1000, eps=1)
    net.plot()"""
    #testgame = GameNim(gameVariables=[5,2])
    #winner = playGame(testgame, net)
    
    player0 = ANET()
    print(player0.forward([2, 1], [1, 2]))
    
    player1 = ANET()
    player1 = torch.load('code/networks/network_50')
    print(player1.forward([2, 1], [1, 2]))
    
    player2 = ANET()
    player2 = torch.load('code/networks/network_90')
    print(player2.forward([2, 1],[1, 2]))
    winner = playGamesAI(1000, player1=player1, player2=player2, verbose=True)
    print(winner)
    



main()