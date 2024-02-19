

class AgentHuman:
    def __init__(self, playerNumber):
        self.playerNumber = playerNumber

    def makeMove(self, gameState, moves):
        print(f"Possible moves: {moves}")
        return int(input("Enter your move: "))