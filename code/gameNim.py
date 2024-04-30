import copy
from game import Game
class GameNim(Game):
    def __init__(self, gameVariables=5, playerTurn=1, maximumMoves=2):
        self.startingState = [playerTurn, gameVariables]
        self.boardState = [playerTurn, gameVariables]
        self.playerTurn = playerTurn
        self.maxMoves = maximumMoves

    def reset(self):
        self.boardState = self.startingState
    
    def update(self, move, verbose=True):
        moves = self.getMoves()
        #print(moves)
        self.boardState[1] -= moves[move]
        if verbose:
            print(f"Player {self.boardState[0]} takes {moves[move]} pieces")
        # Next player's turn
        if self.boardState[0] == 1:
            self.playerTurn = 2
            self.boardState[0] = 2
        else:
            self.playerTurn = 1
            self.boardState[0] = 1
    
    def getMoves(self):
        moves = []
        for i in range(self.maxMoves):
            if i+1 <= self.boardState[1]:
                moves.append(i+1)
        #print(f"Moves: {moves}")
        return moves
    
    def setBoardState(self, boardState):
        self.boardState = copy.deepcopy(boardState)
    
    def getBoardState(self):
        return self.boardState
    
    def printGameState(self):
        print(f"Player {self.boardState[0]}'s turn")
        print(f"Pieces left: {self.boardState[1]}, viable picks: {self.getMoves()}")
    """
    This returns the state where the action has been performed, but makes sure the game is still in the state before the action
    """
    def actionOnState(self, action, board): #-> state
        self.setBoardState(board)
        self.update(action)
        boardState = self.boardState
        self.setBoardState(board)
        return boardState
    
    # Replace with the isFinalState() 
    def isFinalState(self, board=None) -> int or None: # type: ignore
        if board !=None:
            self.setBoardState(board)

        if self.boardState[1] == 0:
            if self.boardState[0] == 2:
                return 1
            else:
                return -1
        else:
            return None
        
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