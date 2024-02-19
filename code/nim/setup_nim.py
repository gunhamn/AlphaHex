from agent_random import AgentRandom
from game_nim import GameNim
from agent_human import AgentHuman

class SetupNim:

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

def main():
    game = GameNim()
    game.reset([15, 3])
    agent1 = AgentRandom(1)
    agent2 = AgentHuman(2)
    setup = SetupNim(game, [agent1, agent2])
    setup.playGame(verbose=True)

main()