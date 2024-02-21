from numpy import random

class AgentRandom:
    def __init__(self, playerNum):
        self.playerNum = playerNum
    
    def makeMove(self, gameState, moves):
        return random.choice(moves)