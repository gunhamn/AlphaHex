import numpy as np
#Tror denne e good
class node:
    def __init__(self, state, action=None, parent=None, maxMoves=2) -> None:
        self.boardState= state
        self.maxMoves = maxMoves
       #self.player = state[1]
        self.children = [] #should contain nodes this is okey, i use append
        self.childVisited = np.zeros(self.maxMoves) #this is hardcoded right now - change to maximum moves for hex???
        self.parent = parent
        self.visited = 0
        self.eval = 0
        self.Q = np.zeros(self.maxMoves) #all these empty lists are a PROBLEM, need possible actions to get correct length
        self.action = action
        #what it should give neural net, should be fixed
        self.net = state
        pass
        #children = np.array(node, node, node) where length equals possible moves to make
        #state
        #value
    
    def exploration(self):
        if self.visited == 0:
            return np.array([np.sqrt(2)]*(self.maxMoves))
        #c = 1
        return np.sqrt(np.log(self.visited)/(1+self.childVisited)) 
    
    def update(self, value, action):
        #print(f"action: {action}")
        """print(f"IN BACKPROP:")
        print(f"state: {self.boardState}")
        for child in self.children:
            print(f"child: {child.boardState}")
        print(f"action {action}")"""
        self.visited+=1
        self.eval+=value
        if action is not None:
            for i in range(len(self.children)):
                if self.children[i].action == action:
                    action=i
            self.childVisited[action]+=1 #Next step
            self.Q[action]=self.eval/self.childVisited[action]
        pass