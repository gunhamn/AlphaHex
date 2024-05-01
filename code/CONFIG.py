import numpy as np

CONFIG = {}

#Hex
CONFIG['boardSize'] = 7

#MCTS parameters
CONFIG['episodes'] = 200
CONFIG['sims'] = 100

#Neural network
CONFIG['numInput'] = (49, 3)
CONFIG['numOutput'] = 49
CONFIG['layers'] = [
    {"type": "Conv1D", "filters": 64, "kernel_size": 3, "padding": "same", "input_shape": (49, 3)},
    {"type": "Conv1D", "filters": 64, "kernel_size": 3, "padding": "same"},
    {"type": "ReLU"},
    {"type": "Flatten"},
    {"type": "Dense", "units": 49, "activation": "softmax"}]
CONFIG['optimizer'] = 'Adam'
CONFIG['learningRate'] = 0.001

#System parameters
CONFIG['trainingEpochs'] = 8 #dont necessarily need
CONFIG['intervalSave'] = 5
CONFIG['TOPPGames'] = 25

