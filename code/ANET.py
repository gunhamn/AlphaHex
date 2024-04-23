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

Input:
- len(boardState)
- the input is the state of the game, which includes the boardstate and which players turn it is
Output:
- len(totalLegalMoves) Not sure if it has to be legal?
- Return a possibility distribution over the possible moves

Need a saving and loading mechanism for the networks, so a parser 

"""

import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch
import matplotlib.pyplot as plt

""" Couldn't get imports to work.....
import tensorflow as tf
import torch
import torch.nn as nn
"""

class ANET(nn.Module):
    def __init__(self, numInput=2, numOutput=2) -> None:
        super(ANET, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(numInput, 10),
            nn.ReLU(),
            nn.Linear(10, 15),
            nn.ReLU(),
            nn.Linear(15, 10),
            nn.ReLU(),
            nn.Linear(10, numOutput),
            nn.Softmax(dim=0)
        )
        
    #I have some issues with torch as i am not used to using it
    def forward(self, x, moves = None):#take in legal moves?
        x = torch.tensor(x, dtype=torch.float32)
        #x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        if moves!=None:
            set1 = set(moves)

            # Iterate over the indices of list2
            for i in range(len(logits)):
                # Check if the index+1 is in list1
                if i + 1 not in set1:
                    # If not, set the value to 0
                    logits[i] = 0
        logits = logits / torch.sum(logits, dim=0, keepdim=True)
        #print(f"logits: {logits}")
        return logits
    
    def train(self, data, batch_size=10, num_epochs=1000, learning_rate = 0.0001) -> None:
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.parameters(), lr=learning_rate)
        print(f"data: {data}")
        lossArray=[]
        for epoch in range(num_epochs):
            # Randomly sample minibatch from replay buffer
            #minibatch = np.random.choice(data, size=batch_size, replace=False)
            # Separate inputs and targets from minibatch cases
            inputs = np.array([case[0] for case in data])
            targets = np.array([case[1] for case in data])

            # Convert inputs and targets to PyTorch tensors
            inputs = torch.tensor(inputs, dtype=torch.float32)
            targets = torch.tensor(targets, dtype=torch.float32)

            # Zero the gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = self(inputs)

            # Compute loss
            loss = criterion(outputs, targets)
            print(f"loss: {loss}")
            lossArray.append(loss.item())

            # Backpropagation
            loss.backward()

            # Update weights
            optimizer.step()
        #print(f"lossArray: {lossArray}")
        #lossArray = lossArray.detach().numpy()
        plt.plot(lossArray)
        plt.show()

        pass