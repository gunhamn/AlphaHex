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
import copy

class GameNim:
    def __init__(self, gameVariables=[5, 2], playerTurn=1, playerCount=2):
        self.boardState = gameVariables
        self.playerTurn = playerTurn
        self.playerCount = playerCount

    def reset(self, gameVariables=[5, 2], playerTurn=1):
        # [N, K]
        # N, the number of pieces on the board
        # K, the max number that a player can take on their turn
        self.boardState = gameVariables
        self.playerTurn = playerTurn
    
    def update(self, move, verbose=False):
        """ Not checking if the move is valid """
        self.boardState[0] -= move
        if verbose:
            print(f"Player {self.playerTurn} takes {move} pieces")
        
        # Next player's turn
        if self.playerTurn == self.playerCount:
            self.playerTurn = 1
        else:
            self.playerTurn += 1
        return self.boardState, self.playerTurn, self.getMoves(), self.PlayerHasWon()
    
    def getMoves(self):
        moves = []
        for i in range(1, self.boardState[1]+1):
            if i <= self.boardState[0]:
                moves.append(i)
        return moves
    
    def setBoardState(self, boardState, playerTurn):
        self.boardState = copy.deepcopy(boardState)
        self.playerTurn = copy.deepcopy(playerTurn)
    
    def getBoardState(self):
        return self.boardState, self.playerTurn
    
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

    def boardStateToANET(self, boardState):
        """ Hex method:
        Takes in a boardState and tranforms it
        into input for the ANET.
        """
        return boardState[0]
    
    def ANETtoLegasMovesList(self, ANEToutput):
        """ Hex method:
        Takes in the ANET output and
        tranforms it into a list of
        all legal and illegal moves.
        """
        return ANEToutput
    
    def actionOnState(self, action, board, player): #-> state
        #print(f"In action input: {board}, {player}")
        self.setBoardState(board, player)
        moves = self.getMoves()
        #remember to check if it ever takes illeagal moves
        """if isinstance(moves, int):
            self.update(moves)
        else:"""
        self.update(moves[action])
        boardState = self.boardState
        playerTurn = self.playerTurn
        #print(f"In action input: {board}, {player}")
        self.setBoardState(board, player)
        #print(f"In action: {self.boardState}, {self.playerTurn}")
        return [boardState, playerTurn]
    
    
    def isFinalState(self, board, player) -> int or None: # type: ignore
        self.setBoardState(board, player)
        #print(f"boardstate: {self.boardState[0]}")
        if self.boardState[0] == 0:
            if self.playerTurn == 2:
                #print(f"is final state: {self.playerTurn-1}")
                return 1
            else:
                #print(f"is final state: {self.playerTurn+1}")
                return -1
        else:
            return None