"""
This class should inherit from the Game class
and implement the methods:
- reset
- update
- getMoves
- setBoardState
- PlayerHasWon
- printGameState
"""

class GameNim:
    def __init__(self):
        self.boardState = None
        self.playerTurn = 0
        self.playerCount = 2

    def reset(self, gameVariables=[15, 2]):
        # [N, K]
        # N, the number of pieces on the board
        # K, the max number that a player can take on their turn
        self.boardState = gameVariables
        self.playerTurn = 1
    
    def update(self, move, verbose=False):
        self.boardState[0] -= move
        if verbose:
            print(f"Player {self.playerTurn} takes {move} pieces")
        
        # Next player's turn
        if self.playerTurn == self.playerCount:
            self.playerTurn = 1
        else:
            self.playerTurn += 1
    
    def getMoves(self):
        moves = []
        for i in range(1, self.boardState[1]+1):
            if i <= self.boardState[0]:
                moves.append(i)
        return moves
    
    def setBoardState(self, boardState, playerTurn):
        self.boardState = boardState
        self.playerTurn = playerTurn
    
    def PlayerHasWon(self):
        if self.boardState[0] == 0:
            # The last player to take pieces won
            if self.playerTurn == 1:
                return self.playerCount
            else:
                return self.playerTurn - 1
        else:
            return 0
    
    def printGameState(self):
        print(f"Player {self.playerTurn}'s turn")
        print(f"Pieces left: {self.boardState[0]}, max pick: {self.boardState[1]}")