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
from tqdm import tqdm

class rl_system:
    def __init__(self, game: GameHex) -> None:
        self.net = None
        self.tree = None
        self.game = game
        self.state = None
        pass

    def train(self, saveI, number_games, number_sim, eps):
        RBUF = []
        #self.net= ANET_tf(numInput=self.game.maxMoves+1, numOutput=self.game.maxMoves)
        for game in range(number_games):
            print(f'its in new game {game}')
            #RBUF = []
            self.game.reset()
            self.state= self.game.getBoardState()
            self.tree = mct(state=self.state, game = GameHex(self.game.boardsize, playerTurn=self.game.boardState[0]), network=self.net)
            while self.game.isFinalState(self.state) == None: #Trenge ikke ta inn parametre
                for sim in tqdm(range(number_sim)):
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

        with open('data.txt', 'w') as file:
            # Iterate over the list and write each element to the file
            for item in RBUF:
                file.write(f"{item}" + '\n') 
       # print(f"data: {RBUF}")
        return 0


    
def main():
    print("RUN BEGINS")
    
    game = GameHex(boardSize=7)
    system = rl_system(game)
    system.train(saveI=5, number_games=1000, number_sim=1500, eps=1)
    
    



main()