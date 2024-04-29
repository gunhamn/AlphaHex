"""
This class should be an empty class that other game classes
inherit from, implementing the following methods:
- reset check
- update check
- getMoves check
- setBoardState check
- PlayerHasWon check
- printGameState check
- getBoardState check
- isFinalState check
- actionOnState check
"""

from abc import abstractmethod


class Game:
    def __init__(self, state) -> None:
        self.state = state
        pass
    """
    Resets the game to the starting point
    """
    @abstractmethod
    def reset(self):
        pass
    """
    Updates the game with move, this will result in the change of the board and also the switch of the player
    """
    @abstractmethod
    def update(self):
        pass
    """
    Gives the legal moves to do in the game
    """
    @abstractmethod
    def getMoves(self):
        pass
    """
    Sets the boardstate
    """
    @abstractmethod
    def setBoardState(self):
        pass
    """
    gives the player who has won
    """
    @abstractmethod
    def PlayerHasWon(self):
        pass
    """
    Prints the gamestate
    """
    @abstractmethod
    def printGameState(self):
        pass
    """
    Gets the boardstate
    """
    @abstractmethod
    def getBoardState(self):
        pass
    """
    Checks if its in final state and gives value 1 for player 1 and -1 for player 2
    """
    @abstractmethod
    def isFinalState(self):
        pass
    """
    Think its the same as update
    """
    @abstractmethod
    def actionOnState(self):
        pass