from alphahex import GameHex
import numpy as np
from ANET_tf import ANET_tf
import keras
class TOPP:
    def __init__(self, networks, game:GameHex) -> None:
        self.score=[0]*len(networks)
        self.game = game
        self.networks = networks
        pass

    def tournament(self, numberOfRounds):
        for i in range(len(self.networks)):
            for j in range(len(self.networks)):
                if self.networks[i]!=self.networks[j]:
                    self.play(self.networks[i], self.networks[j], i, j, numberOfRounds)
                    self.play(self.networks[j], self.networks[i], j, i, numberOfRounds)
        pass

    def play(self, player1, player2, player1Nr, player2Nr, numberOfRounds):
        for gameNr in range(numberOfRounds):
            self.game.reset()
            while self.game.isFinalState()==None:
                if self.game.getBoardState()[0]==1:
                    action = np.argmax(player1.forward(self.game.getBoardState()))
                    self.game.update(move=action)
                else:
                    action = np.argmax(player2.forward(self.game.getBoardState()))
                    self.game.update(move=action)
            if self.game.isFinalState==1:
                self.score[player1Nr]+=1
            else:
                self.score[player2Nr]+=1
        pass

if __name__ == "__main__":
    game = GameHex(boardSize=4)
    numOutput = game.boardsize*game.boardsize
    numInput=numOutput+1

    player1 = ANET_tf(numInput=numInput, numOutput=numOutput)
    player1.model = keras.models.load_model('code/networks/network_5.keras')
    player2 = ANET_tf(numInput=numInput, numOutput=numOutput)
    player2.model = keras.models.load_model('code/networks/network_10.keras')
    player3 = ANET_tf(numInput=numInput, numOutput=numOutput)
    player3.model = keras.models.load_model('code/networks/network_20.keras')
    player4 = ANET_tf(numInput=numInput, numOutput=numOutput)
    player4.model = keras.models.load_model('code/networks/network_50.keras')

    networks=[player1, player2, player3, player4]
    topp = TOPP(networks=networks, game=game)
    topp.tournament(10)
    #plot histogram with score