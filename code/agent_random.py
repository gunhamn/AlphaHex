from numpy import random

class AgentRandom:
    def __init__(self, playerNumber):
        self.playerNumber = playerNumber
    
    def makeMove(self, gameState, moves):
        return random.choice(moves)