from MCT_random import mct
import numpy as np
from alphahex import GameHex

class mctAgent():
        def __init__(self, numer_sim) -> None:
              self.tree = None
              self.number_sim = numer_sim
              pass

        def makeMove(self, game:GameHex):
                    self.tree = mct(state=game.getBoardState(), game = GameHex(boardSize=game.boardsize))
                    #self.tree.root = game.boardState
                    print(f"In makemove tree:")
                    game.printGameState()
                    for sim in range(self.number_sim):
                        self.tree.sim()
                    D = self.tree.distribution()
                    print(f"distribution: {D}")
                    action = np.argmax(D)
                    print(f"action: {action}, actual action: {self.tree.root.children[action].action}")
                    game.update(move=self.tree.root.children[action].action)

class randomAgent():
        def __init__(self) -> None:
              pass

        def makeMove(self, game: GameHex):
            move = np.random.choice(game.getMoves())
            game.update(move=move)

def tournament(player1, player2, game:GameHex, numberGames:int):
        winCount=[0,0]
        for g in range(numberGames):
            game.reset()
            while game.isFinalState()==None:
                        game.printGameState()
                        if game.boardState[0]==1:
                            player1.makeMove(game)
                            print("Player1 has made move")
                            game.printGameState()
                        else:
                            player2.makeMove(game)
            if game.isFinalState()==1:
                winCount[0]+=1
            else:
                  winCount[1]+=1
            game.printGameState()
        return winCount

            


if __name__ == "__main__":
    print("RUNSTART")
    game = GameHex(boardSize=3)
    mctsPlayer = mctAgent(numer_sim=1000)
    randomPlayer = randomAgent()
    #print(game.getMoves())
    win1 = tournament(player1=mctsPlayer, player2=randomPlayer, game=game, numberGames=100)
    game = GameHex(boardSize=3)
    mctsPlayer = mctAgent(numer_sim=1000)
    randomPlayer = randomAgent()
    win2 = tournament(player1=randomPlayer, player2=mctsPlayer, game=game, numberGames=100)
    print(win1)
    print(win2)
    pass