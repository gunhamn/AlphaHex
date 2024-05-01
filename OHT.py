# Import and initialize your own actor
from Code.ANET_tf import ANET_tf
import keras
from Code.alphahex import GameHex
from ActorClient import ActorClient
import numpy as np
class OHT(ActorClient):
    """
    Initializes the class to prepare for OHT
    """

    def __init__(self, auth, qualify):
        super().__init__(auth=auth, qualify=qualify)
        self.game = GameHex(boardSize=7)
        self.actor=ANET_tf(numInput=50, numOutput=49)
        self.actor.model = keras.models.load_model('code/networks/network_0OHT.keras')

    def handle_game_start(self, start_player):
       self.game.reset()
       self.game.boardState[0]=start_player
       pass

    def handle_get_action(self, state):
        self.game.setBoardState(state)

        prediction = self.actor.forward(state, self.game.getMoves())
        values_array = np.array(prediction)
        max_index = np.argmax(values_array)

        # Assuming you want to convert the index to (row, col) indices for a 7x7 grid
        rows = max_index // 7
        cols = max_index % 7
        row = int(rows)
        col= int(cols)
        return row, col
    
    

# Initialize and run your overridden client when the script is executed
if __name__ == '__main__':
 client = OHT(auth='a14d004f33fb4a6c8747363545905d32', qualify=False)
 client.run(mode='league')