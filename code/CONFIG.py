import numpy as np

CONFIG = {}

#Hex
CONFIG['boardSize'] = 4

#MCTS parameters
CONFIG['episodes'] = 5
CONFIG['sims'] = 5

#Neural network
CONFIG['layers'] = [20, 20, 20]
CONFIG['activationFunction'] = ['tanH','tanH','tanH']
CONFIG['rangeInitial'] = [-0.01,0.01] #dont necessarily need
CONFIG['optimizer'] = 'Adam'
CONFIG['learningRate'] = 0.01#0.3

#System parameters
CONFIG['trainingEpochs'] = 8 #dont necessarily need
CONFIG['intervalSave'] = 5
CONFIG['TOPPGames'] = 25

