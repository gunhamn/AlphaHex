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

""" Couldn't get imports to work.....
import tensorflow as tf
import torch
import torch.nn as nn
"""

class ANET(nn.Module):
    def __init__(self, numInput=2, numOutput=2) -> None:
        super(ANET, self).__init__()
        self.fc1 = nn.Linear(numInput, 5)  # Input layer: 2 input nodes, 2 output nodes
        #Can add more layers here, hidden layers and so on using relu or tanH, and a sigmoid at the end?
        self.fc2 = nn.Linear(5, numOutput)
        #Remember to add the layers in the forward pass aswell
        self.softmax = nn.Softmax(dim=1)  # Softmax layer
        
    #I have some issues with torch as i am not used to using it
    def forward(self, x):
        x = torch.tensor(x, dtype=torch.float32)
        x = nn.ReLU(self.fc1(x)) # Fully connected layer
        x = nn.ReLU(self.fc2(x))
        x = self.softmax(x)  # Softmax layer
        return x
    
    def train(self, data, batch_size=10, num_epochs=100, learning_rate = 0.01) -> None:
        criterion = nn.MSELoss()
        optimizer = optim.SGD(self.parameters(), lr=learning_rate)
        print(f"data: {data}")
        for epoch in range(num_epochs):
            # Randomly sample minibatch from replay buffer
            minibatch = np.random.choice(data, size=batch_size, replace=False)
            # Separate inputs and targets from minibatch cases
            inputs = np.array([case[0] for case in minibatch])
            targets = np.array([case[1] for case in minibatch])

            # Convert inputs and targets to PyTorch tensors
            inputs = torch.tensor(inputs, dtype=torch.float32)
            targets = torch.tensor(targets, dtype=torch.float32)

            # Zero the gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = self(inputs)

            # Compute loss
            loss = criterion(outputs, targets)

            # Backpropagation
            loss.backward()

            # Update weights
            optimizer.step()


        pass