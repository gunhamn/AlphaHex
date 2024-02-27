import numpy as np
class node:
    def __init__(self, state, action=None, parent=None) -> None:
        self.boardState= state[0]
        self.player = state[1]
        self.children = [] #should contain nodes
        self.childVisited = []
        self.parent = parent
        self.visited = 0
        self.eval = 0
        self.Q = []
        self.action = action
        #what it should give neural net, should be fixed
        self.net = np.array([state[0][0], state[1]])
        pass
        #children = np.array(node, node, node) where length equals possible moves to make
        #state
        #value
    
    def exploration(self):
        if self.visited == 0:
            return np.sqrt(2)
        #c = 1
        return np.sqrt(np.log(self.visited)/(1+self.childVisited)) 
    
    def update(self, value, action):
        self.visited+=1
        self.eval+=value
        if action is not None:
            self.childVisited[action]+=1
            self.Q[action]=self.eval/self.childVisited[action]
        pass