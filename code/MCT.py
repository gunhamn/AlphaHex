#Emily sin incorporation av Monte Carlo tre
from Node import node
import numpy as np
from gameNim import GameNim
from ANET import ANET
import torch
import torch.nn.functional as F
import random
class mct:
    def __init__(self, state, game: GameNim, network: ANET, eps:float = 1) -> None:
        self.root = node(state)
        self.game = game
        self.net = network
        self.epsilion = eps
        pass

    #tree policy, return leaf node
    def tree_policy(self, state: node) -> node:
        #first check if it has children
        #print(f"Tree policy, boardstate:{state.boardState}, player: {state.player}")
        if len(state.children) == 0 or self.game.isFinalState(state.boardState)!=None:
            return state
        #then check if its player 1 or 2
        #then pick the child and run the tree policy again, until it is a leaf node so no children 

        if len(state.children)==1:
            state = self.tree_policy(state.children[0])
            return state
        
        """ random_number = random.random()
        #print(random_number)
        if random_number < self.epsilion:
                a=random.randint(0, 1)"""

        if state.player == 1:
            

            #maximum player
            # action = np.argmax(Q(s_t, a) + u(s_t, a))
            # print(state.Q + state.exploration())
            #print(f"p1: argmax of: {state.Q + state.exploration()}")
            a = np.argmax(state.Q + state.exploration())
            #What we want is the correct child node
            #update is move
            #getBoardstate to get the updated state
        else:
            #minimum player
            #action = np.argmin(Q(s_t, a) - u(s_t, a))
            #print(f"p2: argmin of: {state.Q + state.exploration()}")
            a = np.argmin(state.Q - state.exploration())
        #print(f"tree_policy action {a}")
        state = self.tree_policy(state.children[a])
        return state

    #expansion, add all children to leaf node, When making children flip what player it is? YES
    def expansion(self, state: node):
        self.game.setBoardState(state.boardState)
        moves = self.game.getMoves()
        if moves == []:
            return state
        #print(f"moves expansion: {moves}")
        #print(f"expansion_1: {self.root.boardState}")
        #print(f"boardSTate in expansion {self.game.getBoardState()}")
        for i in range(len(moves)): # change to "for move in moves:"
            state.children.append(node(self.game.actionOnState(i, state.boardState, state.player), i, state))
            #print(f"expansion_2: {self.root.boardState}")
        #return the first child since thats what the rollout will choose, can rather implement a random
        #print(f"children expanded: {state.children}")
        #print(f"child picked: {np.random.choice(state.children)}")
        return np.random.choice(state.children)

    #Rollout, randomly pick one child to rollout and give that to the neural network and continue until final state, return final value and child, state?
    def rollout(self, state: node) -> int:
        while self.game.isFinalState(state.boardState, state.player)==None:
            #print(self.game.getMoves())
            #print(f"stateNet: {state.net}, stones: {state.boardState[0]}, player: {state.player}")
            action = np.argmax(self.net.forward(state.net, self.game.getMoves() ))
            
            #print(f"rollout, state: {state.boardState}, player: {state.player}")
            #print(f"torch.argmax: {self.net.forward(state.net, self.game.getMoves())}, action: remove {action+1}")
            #print(f"before action state: {state.boardState}")
            #print(f"action {action}")
            #print(f"rollout, state: {state.boardState}, chosen action: {action}, player: {state.player}")
            state = node(self.game.actionOnState(action, state.boardState, state.player))
            #print(f" after rollout, state: {state.boardState}, chosen action: {action}, player: {state.player}")
        return self.game.isFinalState(state.boardState, state.player)
    
    #Backprop, propogate the final value up the tree, and update the visited count 
    def backprop(self, state: node, value: int):
        #print("BACKPROP")
        action = None
        #print(f"state: {state.boardState}")
        #print(f"root: {self.root.boardState}")
        #print(f" action back: {state.action}")
        state.update(value, action)
        while state!=self.root: #this could maybe not work, should work but may not
            action = state.action
            state = state.parent
            state.update(value, action)
            
        pass

    #add all these functions in one func called sim(state), where state is the boardstate or root 
    #does it need to take in state, its just the root?
    #does it need to take in the neural network? to do the rollout 

    def sim(self, eps):

        #print('TREE:')
        #self.print_tree(self.root)
        self.eps=eps # ikke i bruk
        #self.print_tree(self.root)
        #print(f"root_insim: {self.root.boardState}")
        
        # check om denne gör noe
        self.game.setBoardState(self.root.boardState, self.root.player)
        # check om denne gör noe
        #print(f"New simulation, boardstate: {self.root.boardState}, player: {self.root.player}")
        leaf = self.tree_policy(self.root)
        #print(f"leaf: {leaf.boardState}")
        #print(f"root_after_tree_policy: {self.root.boardState}")
        rolloutChild = self.expansion(leaf)
        #print(f"rolloutChild: {rolloutChild.boardState}")
        #print(f"root_after_expansion: {self.root.boardState}")
        value = self.rollout(rolloutChild)
        #print(f"root_after_rollout: {self.root.boardState}")
        self.backprop(rolloutChild, value)
        #print(f"Simulation ended with value: {value}\n")
        

    #getting the distribution of visited count from root
    def distribution(self):
        #should be normalized
        #print(f'Q: {self.root.Q}')
        #arr = np.array(self.root.childVisited)
        #torch.softmax(self.root.Q)
        """print(self.root.Q)
        arr = np.array(self.root.Q)
        total = np.sum(arr)
        if total!=0:
            arr = arr/total"""
        def softmax(x):
            e_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
            return e_x / e_x.sum(axis=0)

        # dist = F.softmax(torch.tensor(self.root.childVisited), dim=0)
        dist = softmax(self.root.childVisited)
        #     dist = np.array(dist)
        #print(dist)
        return list(dist)
        #return list(self.root.childVisited)
    
    def print_tree(self, node, depth=0):
        if node is None:
            return
        # Print current node
        print("  " * depth + f"Node: Player {node.player}, Board State: {node.boardState}, Q: {node.Q}, Exploration: {node.exploration()}, Eval: {node.eval}, childVisited: {node.childVisited}, Visited: {node.visited}")
        
        # Recursively print children
        for child in node.children:
            self.print_tree(child, depth + 1)
