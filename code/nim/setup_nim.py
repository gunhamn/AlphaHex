from agent_random import agent_random
from game_nim import game_nim

# class setup_nim

# Variables:
    # self.game
    # self.agents = [agent1, agent2]

# Functions:
#   __init__(self, game, agents)
#   playGame(self, verbose=True)

class setup_nim:

    def __init__(self, game, agents):
        self.game = game
        self.agents = agents
    
    def playGame(self, verbose=True):
        while self.game.PlayerHasWon() == 0:
            if verbose:
                self.game.printGameState()
            moves = self.game.getMoves()
            move = self.agents[self.game.playerTurn-1].makeMove(self.game, moves)
            self.game.update(move, verbose=verbose)
        if verbose:
            print(f"Player {self.game.PlayerHasWon()} won!")
        return self.game.PlayerHasWon()
    
# main function


def main():
    game = game_nim()
    game.reset([15, 3])
    agent1 = agent_random(1)
    agent2 = agent_random(2)
    setup = setup_nim(game, [agent1, agent2])
    setup.playGame(verbose=True)

main()