#for online tournament needs to work on 7x7 board
"""state= [
2, #player
0,0,0,0,0,0,0, #board
0,0,0,0,0,0,0,
0,0,0,0,0,0,0,
0,0,0,0,0,0,0,
0,0,0,0,0,0,0,
0,0,0,0,0,0,0,
0,0,0,0,0,0,0
]
"""
from cell import Cell

class GameHex:
    def __init__(self, boardSize=7, playerTurn=1, playerCount=2):
        self.startingPlayer = playerTurn
        self.boardsize = boardSize
        self.boardState = self.initializeBoard(boardSize, playerTurn)
        self.playerTurn = playerTurn
        self.playerCount = playerCount

    def initializeBoard(self, size, player):
        board = [player]
        for i in range(size*size):
            new_cell = Cell(position="Center")
            if i < size:
                new_cell.pos="Top"
            elif i >= (size*size)-size:
                new_cell.pos="Bot"
            if i % size == 0:
                new_cell.pos+="Left"
            elif i % size == size - 1:
                new_cell.pos+="Right"
            board.append(new_cell)
        return board

    def reset(self):
        #something to reset the game to startpoint
        self.initializeBoard(self.boardsize, self.startingPlayer)
        pass

    def update(self, move):
        #Updates the board and game based on move
        if self.playerTurn==1:
            self.boardState[move+1] = 1
            self.playerTurn = 2
            self.boardState[0] = 2 #vettkje om dette ska ver en del
        else:
            self.boardState[move+1] = 2
            self.playerTurn = 1
            self.boardState[0] = 1 #vettkje om dette ska ver en del
        pass

    def getMoves(self):
        #gives legal moves to make on the board
        indices_of_zeros = [index for index, value in enumerate(self.boardState) if value == 0]
        return indices_of_zeros

    def setBoardState(self):
        #set the boardstate
        pass
    
    def PlayerHasWon(self):
        #Needs to check if the game is in a final state, and what player has won
        pass
    
    def printGameState(self):
        #Print state to get overview, here the board needs to be printed
        print(f"Player {self.boardState[0]}'s turn")
        elements = self.boardState[1:]
        grid = [elements[i*7:i*7+7] for i in range(7)]

        rows = len(grid)
        cols = len(grid[0])

        # Initialize an empty list to store the strings
        strings = []

        # Iterate over the rows and columns of the grid
        for i in range(rows):
            string =":"+" " * (12 - (2 * i))  # Calculate leading spaces based on row index
            for j in range(i + 1):
                string += f"{grid[i-j][j]}" + " " * 3  # Add elements from the grid with padding
            strings.append(string.strip())  # Remove trailing spaces and add string to the list
            
        # Iterate over the rows and columns of the grid
        for i in range(rows, 0, -1):
            #print(i)
            string =":"+" " * (16 - (2*i))  # Calculate leading spaces based on row index
            #print("NEW LINE")
            for j in range(i-1):
                #print(f"i: {i}, j:{j}")
                #print(f"box 1: {rows-1-j}, box2: {7 - (i-1-1*j)}")
                string += f"{grid[rows-1-j][7 - (i-1-1*j)]}" + " " * 3  # Add elements from the grid with padding
                #print(string)
            strings.append(string.strip())  # Remove trailing spaces and add string to the list


        # Join the strings with newline characters
        result = "\n".join(strings)

        print(result)

        

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
        #transforms it to the move
        return ANEToutput
    
    def isFinalState(self, board, player) -> int or None: # type: ignore
        #check if its final state
        pass


if __name__ == "__main__":
    game = GameHex()
    game.printGameState()
    game.update(3)
    game.printGameState()