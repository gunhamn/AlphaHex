from numpy import random

# class agent_random

# variables
#   self.playerNumber

# functions
#   __init__(self, playerNumber)
#   makeMove(self, gameState, moves)


class agent_random:
    def __init__(self, playerNumber):
        self.playerNumber = playerNumber
    
    def makeMove(self, gameState, moves):
        return random.choice(moves)