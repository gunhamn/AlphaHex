from alphahex import GameHex
from ANET_tf import ANET_tf
from MCT_random import mct
from RL_system import rl_system
from TOPP import TOPP
from CONFIG import CONFIG
import keras
import matplotlib.pyplot as plt
"""
Training networks with reinforcement learning
"""
def trainNetworks(filename: str, system: rl_system):
    system.train(saveI=CONFIG.get('intervalSave'), number_games=CONFIG.get('episodes'), number_sim=CONFIG.get('sims'), filename=filename)
    pass
"""
Using networks shortly trained in tournament
"""
def shortTopp(game):
    numOutput = CONFIG.get('boardSize')*CONFIG.get('boardSize')
    numInput=numOutput+1
    player1 = ANET_tf(numInput=numInput, numOutput=numOutput)
    player1.model = keras.models.load_model('code/networks/network_5.keras')
    player2 = ANET_tf(numInput=numInput, numOutput=numOutput)
    player2.model = keras.models.load_model('code/networks/network_20.keras')
    player3 = ANET_tf(numInput=numInput, numOutput=numOutput)
    player3.model = keras.models.load_model('code/networks/network_50.keras')
    player4 = ANET_tf(numInput=numInput, numOutput=numOutput)
    player4.model = keras.models.load_model('code/networks/network_100.keras')
    networks=[player1, player2, player3, player4]
    topp = TOPP(networks=networks, game=game)
    topp.tournament(numberOfRounds=CONFIG.get('TOPPGames'))
    print(topp.score)

    plt.bar([1,2,3,4], topp.score, color='blue')
    plt.xlabel('players')
    plt.ylabel('wins')
    plt.title('_/150')
    plt.grid(True)  # Add grid lines for better readability
    plt.show()
    pass


if __name__ == "__main__":
    game = GameHex
    net = ANET_tf
    tree = mct
    actualGame=game(boardSize=CONFIG.get('boardSize'))
    system = rl_system(game=actualGame, gameMaker=game, netMaker=net, treeMaker=tree)
    trainNetworks(filename="OHT", system=system)
    pass