# class game_nim
#   class game_nim

# Variables:
#   self.boardState
#   self.playerTurn

# Functions:
#   __init__(self)
#   reset(self, gameVariables=[N, K])
#   update(self, move)
#   getMoves(self)
#   setBoardState(self, boardState, playerTurn)
#   PlayerHasWon(self), returns 0 if no winner, 1 if player 1 wins, 2 if player 2 wins, and so on..
#   printGameState(self)

class game_nim:
    def __init__(self):
        self.boardState = None
        self.playerTurn = 0
        self.numPlayers = 2

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
        if self.playerTurn == self.numPlayers:
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
                return self.numPlayers
            else:
                return self.playerTurn - 1
        else:
            return 0
    
    def printGameState(self):
        print(f"Player {self.playerTurn}'s turn")
        print(f"Pieces left: {self.boardState[0]}, max pick: {self.boardState[1]}")