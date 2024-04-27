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
from game import Game

class GameHex (Game):
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
        self.adding_neigbors(board)

        return board
    
    def adding_neigbors(self, board):
        #add the neighbors
        grid = [board[1:][i*self.boardsize:i*self.boardsize+self.boardsize] for i in range(self.boardsize)]
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                node = grid[row][col]
                if "Top" in node.pos and "Left" in node.pos:
                    node.neigbors.append(grid[row][col+1])
                    node.neigbors.append(grid[row +1][col])
                    node.neigbors.append(grid[row +1][col+1])
                elif "Top" in node.pos and "Right" in node.pos:
                    node.neigbors.append(grid[row][col-1])
                    node.neigbors.append(grid[row +1][col])
                elif "Top" in node.pos:
                    node.neigbors.append(grid[row][col+1])
                    node.neigbors.append(grid[row][col-1])
                    node.neigbors.append(grid[row+1][col])
                    node.neigbors.append(grid[row+1][col+1])
                elif "Bot" in node.pos and "Left" in node.pos:
                    node.neigbors.append(grid[row][col+1])
                    node.neigbors.append(grid[row - 1][col])
                elif "Bot" in node.pos and "Right" in node.pos:
                    node.neigbors.append(grid[row][col-1])
                    node.neigbors.append(grid[row-1][col])
                    node.neigbors.append(grid[row-1][col-1])
                elif "Bot" in node.pos:
                    node.neigbors.append(grid[row-1][col-1])
                    node.neigbors.append(grid[row][col-1])
                    node.neigbors.append(grid[row][col+1])
                    node.neigbors.append(grid[row-1][col])
                elif "Left" in node.pos:
                    node.neigbors.append(grid[row+1][col])
                    node.neigbors.append(grid[row-1][col])
                    node.neigbors.append(grid[row][col+1])
                    node.neigbors.append(grid[row+1][col+1])
                elif "Right" in node.pos:
                    node.neigbors.append(grid[row+1][col])
                    node.neigbors.append(grid[row-1][col])
                    node.neigbors.append(grid[row][col-1])
                    node.neigbors.append(grid[row-1][col-1])
                elif "Center" in node.pos:
                    node.neigbors.append(grid[row+1][col])
                    node.neigbors.append(grid[row-1][col])
                    node.neigbors.append(grid[row][col-1])
                    node.neigbors.append(grid[row][col+1])
                    node.neigbors.append(grid[row-1][col-1])
                    node.neigbors.append(grid[row+1][col+1])

                print(f"Node: {node.pos}, neighbors: {len(node.neigbors)}")

                


    def reset(self):
        #something to reset the game to startpoint
        self.initializeBoard(self.boardsize, self.startingPlayer)
        pass

    def update(self, move):
        #Updates the board and game based on move
        if self.playerTurn==1:
            self.boardState[move+1].value = 1
            self.playerTurn = 2
            self.boardState[0] = 2 #vettkje om dette ska ver en del
        else:
            self.boardState[move+1].value = 2
            self.playerTurn = 1
            self.boardState[0] = 1 #vettkje om dette ska ver en del
        pass

    def getMoves(self):
        #gives legal moves to make on the board
        indices_of_zeros = [index for index, value in enumerate(self.boardState) if value == 0]
        return indices_of_zeros

    def setBoardState(self, player, board):
        self.boardState=self.setBoard(newBoard=board, player=player)
        #set the boardstate
        pass

    def setBoard(self, newBoard, player):
        board=[player]
        for i in range(len(newBoard)):
            new_cell = Cell(position="Center", value=newBoard[i])
            if i < self.boardsize:
                new_cell.pos="Top"
            elif i >= (self.boardsize*self.boardsize)-self.boardsize:
                new_cell.pos="Bot"
            if i % self.boardsize == 0:
                new_cell.pos+="Left"
            elif i % self.boardsize == self.boardsize - 1:
                new_cell.pos+="Right"
            board.append(new_cell)
        self.adding_neigbors(board)
        return board

    
    def PlayerHasWon(self):
        #Needs to check if the game is in a final state, and what player has won
        pass
    
    def printGameState(self):
        #Print state to get overview, here the board needs to be printed
        print(f"Player {self.boardState[0]}'s turn")
        elements = self.boardState[1:]
        grid = [elements[i*self.boardsize:i*self.boardsize+self.boardsize] for i in range(self.boardsize)]

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
                string += f"{grid[rows-1-j][self.boardsize - (i-1-1*j)]}" + " " * 3  # Add elements from the grid with padding
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
        elements = self.boardState[1:]
        grid = [elements[i*self.boardsize:i*self.boardsize+self.boardsize] for i in range(self.boardsize)]
        for node in elements:
            if "Top" in node.pos:
                if node.value == 2:
                    truth=self.checkNeighbors_2(node, node.neigbors, "Bot")
                    print(truth)
                    if truth:
                        return -1 #?
            if "Left" in node.pos:
                if node.value == 1:
                    truth=self.checkNeighbors_2(node, node.neigbors, "Right")
                    print(truth)
                    if truth:
                        return 1 #?
        return None



        #check if its final state
        pass

    def checkNeighbors_2(self, node: Cell, neighbors: list, pos:str):
        truth=False
        print(f"before check: {node.pos}")
        if pos in node.pos:
            return True
        print("Node:")
        for neigh in node.neigbors:
            print(f"value_ {neigh.value}, pos:{neigh.pos}")
        for neigh in node.neigbors:
            if neigh.value == node.value:
                #print(neigh.value)
                truth = self.checkNeighbors_2(neigh, neigh.neigbors.remove(node), pos)
                #needs to check if it has been checked
        return truth
        pass


if __name__ == "__main__":
    game = GameHex(boardSize=3)
    game.printGameState()
    game.setBoardState(player=1, board=[0 , 0, 0,
0, 1, 0,
0, 0, 0
])
    game.printGameState()
    value = game.isFinalState(board=game.boardState[1:], player=game.boardState[0])
    print(value)



"""
test games:

player 1 should win:
[1 , 1, 1,
2, 2, 0,
0, 0, 0
]

player 2 should win:
[2 , 1, 1,
2, 2, 0,
2, 0, 0
]

is not a finalstate:
[0 , 0, 0,
0, 0, 0,
0, 0, 0
]


"""