import numpy as np
#Tror denne e good
class node:
    def __init__(self, state, maxMoves=2, action=None, parent=None) -> None:
        self.boardState= state
       #self.player = state[1]
        self.children = [] #should contain nodes this is okey, i use append
        self.childVisited = np.zeros(maxMoves) #this is hardcoded right now - change to maximum moves for hex???
        self.parent = parent
        self.visited = 0
        self.eval = 0
        self.Q = np.zeros(maxMoves) #all these empty lists are a PROBLEM, need possible actions to get correct length
        self.action = action
        #what it should give neural net, should be fixed
        self.net = state
        pass
        #children = np.array(node, node, node) where length equals possible moves to make
        #state
        #value
    
    def exploration(self):
        if self.visited == 0:
            return np.array([np.sqrt(2),np.sqrt(2)])
        #c = 1
        return np.sqrt(np.log(self.visited)/(1+self.childVisited)) 
    
    def update(self, value, action):
        #print(f"action: {action}")
        self.visited+=1
        self.eval+=value
        if action is not None:
            self.childVisited[action]+=1 #Next step
            self.Q[action]=self.eval/self.childVisited[action]
        pass