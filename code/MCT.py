#Emily sin incorporation av Monte Carlo tre
from Node import node
import numpy as np
from game_nim import GameNim
from ANET import ANET
class mct:
    def __init__(self, state, game: GameNim, network: ANET) -> None:
        self.root = node(state)
        self.game = game
        self.net = network
        pass

    #tree policy, return leaf node
    def tree_policy(self, state: node) -> node:
        #first check if it has children
        if len(state.children) == 0:
            return state
        #then check if its player 1 or 2
        #then pick the child and run the tree policy again, until it is a leaf node so no children 
        if state.player == 1:
            #maximum player
            # action = np.argmax(Q(s_t, a) + u(s_t, a))
            a = np.argmax(state.Q + state.exploration())
            #What we want is the correct child node
            #update is move
            #getBoardstate to get the updated state
        else:
            #minimum player
            #action = np.argmin(Q(s_t, a) - u(s_t, a))
            a = np.argmin(state.Q - state.exploration())
        state = self.tree_policy(state.children[a])
        #return state

    #expansion, add all children to leaf node, When making children flip what player it is? YES
    def expansion(self, state: node):
        self.game.setBoardState(state.boardState, state.player)
        moves = self.game.getMoves()
        for i in range(len(moves)):
            state.children.append(node(self.game.actionOnState(moves[i], state.boardState, state.player), i, state))
        #return the first child since thats what the rollout will choose, can rather implement a random
        return state.children[0]

    #Rollout, randomly pick one child to rollout and give that to the neural network and continue until final state, return final value and child, state?
    def rollout(self, state: node) -> int:
        while self.game.isFinalState(state.boardState, state.player)!=None:
            action = np.argmax(self.net.forward(state.net))
            self.game.setBoardState(state.boardState, state.player)
            moves = self.game.getMoves()
            state = node(self.game.actionOnState(moves[action], state.boardState, state.player))
        return self.game.isFinalState(state.boardState, state.player)
    
    #Backprop, propogate the final value up the tree, and update the visited count 
    def backprop(self, state: node, value: int):
        action = None
        while state!=self.root: #this could maybe not work, should work but may not
            state.update(value, action)
            action = state.action
            state = state.parent
        pass

    #add all these functions in one func called sim(state), where state is the boardstate or root 
    #does it need to take in state, its just the root?
    #does it need to take in the neural network? to do the rollout 

    def sim(self):
        leaf = self.tree_policy(self.root)
        rolloutChild = self.expansion(leaf)
        value = self.rollout(rolloutChild)
        self.backprop(rolloutChild, value)

    #getting the distribution of visited count from root
    def distribution(self):
        #should be normalized
        arr = np.array(self.root.childVisited)
        total = np.sum(arr)
        if total!=0:
            arr = arr/total
        return arr
