import numpy as np

CONFIG = {}

#Hex
CONFIG['boardSize'] = 4

#MCTS parameters
CONFIG['episodes'] = 3
CONFIG['sims'] = 3

#Neural network
CONFIG['numInput'] = (16, 3)
CONFIG['numOutput'] = 16
CONFIG['layers'] = [
    {"type": "Conv1D", "filters": 64, "kernel_size": 3, "padding": "same", "input_shape": (16, 3)},
    {"type": "Conv1D", "filters": 64, "kernel_size": 3, "padding": "same"},
    {"type": "ReLU"},
    {"type": "Flatten"},
    {"type": "Dense", "units": 16, "activation": "softmax"}]
CONFIG['optimizer'] = 'Adam'
CONFIG['learningRate'] = 0.0001
# Example of a different network architecture
"""
CONFIG['layers'] = [
    {"type": "Flatten", "input_shape": (16, 3)},
    {"type": "Dense", "units": 64, "activation": "tanh"},
    {"type": "Dense", "units": 16, "activation": "sigmoid"}]
CONFIG['optimizer'] = 'adagrad'
CONFIG['learningRate'] = 0.001"""


#System parameters
CONFIG['trainingEpochs'] = 8 #dont necessarily need
CONFIG['intervalSave'] = 1
CONFIG['TOPPGames'] = 25

