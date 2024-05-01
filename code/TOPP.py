from alphahex import GameHex
import numpy as np
from ANET_tf import ANET_tf
import keras
import matplotlib.pyplot as plt
from tqdm import tqdm
class TOPP:
    def __init__(self, networks, game) -> None:
        self.score=[0]*len(networks)
        self.game = game
        self.networks = networks
        pass

    def tournament(self, numberOfRounds):
        networks = self.networks
        num_networks = len(networks)
        
        for i in tqdm(range(num_networks)):
            for j in range(i + 1, num_networks):  # Iterate over remaining networks
                self.play(networks[i], networks[j], i, j, numberOfRounds)
                self.play(networks[j], networks[i], j, i, numberOfRounds)
        pass

    def play(self, player1, player2, player1Nr, player2Nr, numberOfRounds):
        for gameNr in range(numberOfRounds):
            #print(f"Game {gameNr}, player1: {player1Nr}, player2, {player2Nr}")
            self.game.reset()
            while self.game.isFinalState()==None:
                #self.game.printGameState()
                if self.game.getBoardState()[0]==1:
                    action = np.argmax(player1.forward(self.game.getBoardState(), self.game.getMoves()))
                    #print(f"action: {action}")
                    self.game.update(move=action)
                else:
                    action = np.argmax(player2.forward(self.game.getBoardState(), self.game.getMoves()))
                    self.game.update(move=action)
            #print(f"finalstate: {self.game.isFinalState()}")
            if self.game.isFinalState()==1:
                #print("player 1 won")
                self.score[player1Nr]+=1
            else:
                #print("player 2 won")
                self.score[player2Nr]+=1
        print(f"score {self.score}, player1 {player1Nr}, player2 {player2Nr}, numberofGames: {numberOfRounds}")
        pass

if __name__ == "__main__":
    game = GameHex(boardSize=4)
    numOutput = game.boardsize*game.boardsize
    numInput=numOutput

    player1 = ANET_tf(numInput=(numInput,3), numOutput=numOutput)
    player1.model = keras.models.load_model('code/networks/network_0OHT.keras')
    player2 = ANET_tf(numInput=(numInput,3), numOutput=numOutput)
    player2.model = keras.models.load_model('code/networks/network_50OHT.keras')
    player3 = ANET_tf(numInput=(numInput,3), numOutput=numOutput)
    player3.model = keras.models.load_model('code/networks/network_100OHT.keras')
    player4 = ANET_tf(numInput=(numInput,3), numOutput=numOutput)
    player4.model = keras.models.load_model('code/networks/network_130OHT.keras')

    networks=[player1, player2, player3, player4]
    topp = TOPP(networks=networks, game=game)
    print("RUNBEGINS")
    topp.tournament(numberOfRounds=25)
    print(topp.score)

    plt.bar([1,2,3,4], topp.score, color='blue')
    plt.xlabel('players')
    plt.ylabel('wins')
    plt.title('_/150')
    plt.grid(True)  # Add grid lines for better readability
    plt.show()
    #plot histogram with score