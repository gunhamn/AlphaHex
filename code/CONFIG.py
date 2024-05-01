import numpy as np

CONFIG = {}

#Hex
CONFIG['boardSize'] = 4

#MCTS parameters
CONFIG['episodes'] = 200
CONFIG['sims'] = 10

#Neural network
CONFIG['numInput'] = (16, 3)
CONFIG['numOutput'] = 16
CONFIG['layers'] = None
"""[
    {"type": "Conv1D", "filters": 64, "kernel_size": 3, "padding": "same", "input_shape": (49, 3)},
    {"type": "Conv1D", "filters": 64, "kernel_size": 3, "padding": "same"},
    {"type": "ReLU"},
    {"type": "Flatten"},
    {"type": "Dense", "units": 49, "activation": "softmax"}]"""
CONFIG['optimizer'] = 'Adam'
CONFIG['learningRate'] = 0.001

#System parameters
CONFIG['trainingEpochs'] = 8 #dont necessarily need
CONFIG['intervalSave'] = 5
CONFIG['TOPPGames'] = 25

