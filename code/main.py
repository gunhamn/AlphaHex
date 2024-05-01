from alphahex import GameHex
from ANET_tf import ANET_tf
from MCT_random import mct
from RL_system import rl_system
from TOPP import TOPP
from CONFIG import CONFIG
"""
Training networks with reinforcement learning
"""
def trainNetworks(filename: str, system: rl_system):
    system.train(saveI=CONFIG.get('intervalSave'), number_games=CONFIG.get('episodes'), number_sim=CONFIG.get('sims'), filename=filename)
    pass
"""
Using networks shortly trained in tournament
"""
def shortTopp():
    pass
"""
Using networks long trained in tournament   
"""
def longTopp():
    pass

if __name__ == "__main__":
    game = GameHex
    net = ANET_tf
    tree = mct
    actualGame=game(boardSize=CONFIG.get('boardSize'))
    system = rl_system(game=actualGame, gameMaker=game, netMaker=net, treeMaker=tree)
    trainNetworks(filename="OHT", system=system)
    pass