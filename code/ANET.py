"""
Project description:
In this project, a neural network – a.k.a. the actor network
(ANET) – constitutes the target policy. It takes a board
state as input and produces a probability distribution
over all possible moves (from that state) as output.
The main goal of On-Policy MCTS is to produce an
intelligent target policy, which can then be used
independently of MCTS as an actor module.

The class agent_MCT uses the line:
move = max(node.untriedMoves, key=lambda x: self.ANET.predict(node.boardState, node.playerNum, x))
Then ANET should have the method:
predict(node.boardState, move)
That returns the expected value of that move.
"""

class ANET:
    def __init__(self) -> None:
        pass