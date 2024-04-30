#Emily sin incorporation av Monte Carlo tre
from Node import node
import numpy as np
from alphahex import GameHex
from ANET_tf import ANET_tf
import torch
import torch.nn.functional as F
import tensorflow as tf
import random
class mct:
    def __init__(self, state, game: GameHex) -> None:
        self.game = game
        self.game.setBoardState(state)
        self.root = node(state, maxMoves=len(game.getMoves()))

        pass

    #tree policy, return leaf node
    def tree_policy(self, state: node) -> node:
        #print(f"tree_policy state: {state.boardState}")
        #first check if it has children
        if len(state.children) == 0 or self.game.isFinalState(state.boardState)!=None:
            return state
        #then check if its player 1 or 2
        #then pick the child and run the tree policy again, until it is a leaf node so no children 

        if len(state.children)==1:
            state = self.tree_policy(state.children[0])
            return state

        if state.boardState[0] == 1:
            

            #maximum player
            #print(state.Q + state.exploration())
            a = np.argmax(state.Q + state.exploration())
            #What we want is the correct child node
            #update is move
            #getBoardstate to get the updated state
        else:
            #minimum player
            a = np.argmin(state.Q - state.exploration())
        for i in range(len(state.children)):
            """if state.children[i].action==a:
                a=i"""
            #print(f"child: {state.children[i].boardState}")
        #print(f"action: {a}")
        state = self.tree_policy(state.children[a])
        return state

    #expansion, add all children to leaf node, When making children flip what player it is? YES
    def expansion(self, state: node):
        self.game.setBoardState(state.boardState)
        moves = self.game.getMoves()
        if moves == []:
            return state
        if len(state.children)==0:
            for move in moves: # change to "for move in moves:"
                state.children.append(node(self.game.actionOnState(move, state.boardState), move, state, maxMoves=len(self.game.getMoves())-1))
        return np.random.choice(state.children)

    #Rollout, randomly pick one child to rollout and give that to the neural network and continue until final state, return final value and child, state?
    def rollout(self, state: node) -> int:
        #print('IN ROLLOUT')
        while self.game.isFinalState(state.boardState)==None:
            #print(f"possible moves: {self.game.getMoves()}")

            action = np.random.choice(self.game.getMoves())
            
            #print(f"action: {action}")
            #action = np.argmax(self.net.forward(state.boardState, self.game.getMoves() ))
            state = node(self.game.actionOnState(action, state.boardState),maxMoves=len(self.game.getMoves())-1)
        return self.game.isFinalState(state.boardState)
    
    #Backprop, propogate the final value up the tree, and update the visited count 
    def backprop(self, state: node, value: int):
        action = None
        state.update(value, action)
        while state!=self.root:
            action = state.action
            state = state.parent
            state.update(value, action)
            
        pass

    #add all these functions in one func called sim(state), where state is the boardstate or root 
    #does it need to take in state, its just the root?
    #does it need to take in the neural network? to do the rollout 

    def sim(self):
        print("Start of sim")

        """print('TREE:')
        self.print_tree(self.root)"""
        # check om denne gör noe
        self.game.setBoardState(self.root.boardState)
        print(f"root: {self.root.boardState}")
        # check om denne gör noe
        leaf = self.tree_policy(self.root)
        print(f"leaf: {leaf.boardState}")
        rolloutChild = self.expansion(leaf)
        print(f"rolloutChild: {rolloutChild.boardState}")
        value = self.rollout(rolloutChild)
        print("rollout done")
        self.backprop(rolloutChild, value)
        

    #getting the distribution of visited count from root
    def distribution(self):
        #should be normalized
        """print(self.root.Q)
        arr = np.array(self.root.Q)
        total = np.sum(arr)
        if total!=0:
            arr = arr/total"""
        """ def softmax(x):
            e_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
            return e_x / e_x.sum(axis=0)"""

        # dist = F.softmax(torch.tensor(self.root.childVisited), dim=0)
        #dist = softmax(self.root.childVisited)
        dist = tf.nn.softmax(self.root.childVisited)
        dist = np.array(dist)
        """result = [0]*self.game.maxMoves
        
        for i in range(len(self.root.children)):
            if self.root.children[i]."""
        #print(dist)
        return list(dist)
        #return list(self.root.childVisited)
    
    def print_tree(self, node, depth=0):
        if node is None:
            return
        # Print current node
        print("  " * depth + f"Board State: {node.boardState}, Q: {node.Q}, Exploration: {node.exploration()}, Eval: {node.eval}, childVisited: {node.childVisited}, Visited: {node.visited}")
        
        # Recursively print children
        for child in node.children:
            self.print_tree(child, depth + 1)
