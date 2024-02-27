"""
This class should be an empty class that other game classes
inherit from, implementing the following methods:
- reset
- update
- getMoves
- setBoardState
- PlayerHasWon
- printGameState
"""

class Game:
    def __init__(self, state) -> None:
        self.state = state
        pass

    def reset(self):
        pass

    def update(self):
        pass

    def setBoardState(self):
        pass

    def finalState(self):
        pass