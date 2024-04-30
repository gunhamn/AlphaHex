from ANET import ANET
from gameNim import GameNim
from alphahex import GameHex
from ANET_tf import ANET_tf
#from game_nim import GameNim
from MCT_random import mct
import numpy as np
from agent_human import AgentHuman
import torch
import keras
import os
from tensorflow import keras
from keras.models import load_model

class rl_system:
    def __init__(self, game: GameHex) -> None:
        self.net = None
        self.tree = None
        self.game = game
        self.state = None
        pass

    def train(self, saveI, number_games, number_sim, eps):
        RBUF = []
        self.net= ANET_tf(numInput=self.game.maxMoves+1, numOutput=self.game.maxMoves)
        for game in range(number_games):
            print(f'its in new game {game}')
            #RBUF = []
            self.game.reset()
            self.state= self.game.getBoardState()
            self.tree = mct(state=self.state, game = GameHex(self.game.boardsize, playerTurn=self.game.boardState[0]), network=self.net)
            while self.game.isFinalState(self.state) == None: #Trenge ikke ta inn parametre
                for sim in range(number_sim):
                    self.tree.sim()
                D = self.tree.distribution()
                RBUF.append([self.tree.root.boardState, D])
                action = np.argmax(D)
                self.state = self.game.actionOnState(action, self.state)
                chosenChild=None
                for child in self.tree.root.children:
                    if child.action == action:
                        chosenChild = child
                self.tree.root = chosenChild
            #print(f"RBUF: {RBUF.shape}")
            self.net.train(RBUF)
            if (game+1) % saveI == 0:
                #save ANET for tournament play
                self.net.save(f"code/networks/network_{game+1}.keras")
                #torch.save(self.net, f"code/networks/network_{game}")
                pass
        with open('output.txt', 'w') as file:
            # Iterate over the list and write each element to the file
            for item in RBUF:
                file.write(f"{item}" + '\n') 
       # print(f"data: {RBUF}")
        return self.net

def playGame(game: GameNim, network: ANET_tf, verbose=True):
        agent = AgentHuman(2)
        while game.isFinalState() == None:
            if verbose:
                game.printGameState()
            moves = game.getMoves()
            state = game.getBoardState()
            if game.playerTurn == 1:
                #netState= [state[0][0], 1]
                #print(f"state: {network.forward(netState, moves=moves)}")
                action = np.argmax(network.forward(state))
                game.update(action, verbose=verbose)
            else:
                move = agent.makeMove(game, moves)
                game.update(move, verbose=verbose)
        if verbose:
            print(f"Player {game.PlayerHasWon()} won!")
        return game.PlayerHasWon()

def playGamesAI(numberGames: int, player1: ANET_tf, player2: ANET_tf, verbose=True):
        wincount = [0,0]
        for i in range(numberGames):
            game = GameNim(gameVariables=5)
            if i % 2 == 0:
                while game.isFinalState() == None:
                    if verbose:
                        game.printGameState()
                    state = game.getBoardState()
                    if state[0] == 1:
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = np.argmax(player1.forward(state))
                        game.update(action, verbose=verbose)
                    else:
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = np.argmax(player2.forward(state))
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
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = np.argmax(player2.forward(state))
                        game.update(action, verbose=verbose)
                    else:
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = np.argmax(player1.forward(state))
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
    
    """game = GameHex(boardSize=4)
    system = rl_system(game)
    net = system.train(saveI=5, number_games=10, number_sim=100, eps=1)
    net.plot()"""
    #testgame = GameNim(gameVariables=[5,2])
    #winner = playGame(testgame, net)
    player5 = ANET_tf()
    player5.model = keras.models.load_model('code/networks/network_5.keras')
    print(player5.forward([2, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0]))
    player10 = ANET_tf()
    player10.model = keras.models.load_model('code/networks/network_10.keras')
    print(player10.forward([2, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0]))
    """playerN = ANET_tf()
    print(playerN)
    print(playerN.simpleForward([5, 1]))
    playerN.load("code/networks/network_100.keras")
    print(playerN.simpleForward([5, 1]))
    playerN.model = keras.models.load_model('code/networks/network_5.keras')
    print(playerN.simpleForward([1, 5]))
    player1 = ANET_tf()
    player1.model = keras.models.load_model('code/networks/network_10.keras')
    print(player1.simpleForward([1, 5]))"""
    """player0 = ANET()
    player0 = torch.load('code/networks/network_0')
    print(f'code/networks/network_0 {player0.simpleForward([1, 2])}')

    player5 = ANET()
    player5 = torch.load('code/networks/network_5')
    print(f'code/networks/network_5 {player5.simpleForward([1, 2])}')

    # player10 = load_model('code/networks/network_10.keras', custom_objects={'ANET_tf': ANET_tf})
    player10 = ANET_tf()
    player10.build((None, 2))
    player10.load_weights('code/networks/network_10.keras')
    print(f'code/networks/network_10 {player10.predict(np.array([2, 1]))}')

    player200 = ANET()
    player200 = torch.load('code/networks/network_200')
    print(f'code/networks/network_200 {player200.simpleForward([1, 2])}')"""
    # winner = playGamesAI(1000, player1=player1, player2=player2, verbose=True)
    # print(winner)
    



main()