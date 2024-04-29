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
import tensorflow as tf

""" Couldn't get imports to work.....
import tensorflow as tf
import torch
import torch.nn as nn
"""

class ANET(nn.Module):
    def __init__(self, numInput=2, numOutput=2) -> None:
        super(ANET, self).__init__()
        self.lossarray=[]
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
    
    def simpleForward(self, x):
        x = torch.tensor(x, dtype=torch.float32)
        logits = self.linear_relu_stack(x)
        return logits

    def train(self, data, batch_size=10, num_epochs=50, learning_rate = 0.001) -> None:
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.parameters(), lr=learning_rate)
        #print(f"data: {data}")
        lossArray=[]
        if batch_size > len(data):
            # If batch size is larger than buffer size, reduce batch size
            batch_size = len(data)
        #print(data)
        indices = np.random.choice(len(data), batch_size, replace=False)
        minibatch = [data[idx] for idx in indices]
        #minibatch = data
        #print(f"MINIBATCH: {minibatch}")
        for epoch in range(num_epochs):
            # Randomly sample minibatch from replay buffer
            #minibatch = np.random.choice(data, size=batch_size, replace=False)
            # Separate inputs and targets from minibatch cases
            inputs = np.array([case[0] for case in minibatch])
            targets = np.array([case[1] for case in minibatch])

            # print(f"inputs: {inputs}")
            # print(f"targets: {targets}")

            # Convert inputs and targets to PyTorch tensors
            inputs = torch.tensor(inputs, dtype=torch.float32)
            targets = torch.tensor(targets, dtype=torch.float32)

            # Zero the gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = self(inputs)
            # print(f"outputs: {outputs}")
            #print(f"outputs: {torch._softmax(outputs, dim=0, half_to_float=False)}")

            # Compute loss
            loss = criterion(outputs, targets)

            # print(f"loss: {loss}")
            self.lossarray.append(loss.item())
            lossArray.append(loss.item())

            # Backpropagation
            loss.backward()

            # Update weights
            optimizer.step()
        #print(f"lossArray: {lossArray}")
        """plt.plot(lossArray)
        plt.show()"""
        #lossArray = lossArray.detach().numpy()

        pass

    def plot(self):
        plt.plot(self.lossarray)
        plt.show()




if __name__ == "__main__":
    net = ANET()
    data = [[[2, 1], [0, 1]]]*2000
    # print(data)
    net.train(data)
    print(net.simpleForward([2, 1]))
    net.plot()
    
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, input_shape=(2,), activation='relu'),
        tf.keras.layers.Dense(15, activation='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(2, activation='softmax')
    ])
    data = np.array(data)
    x = data[:, 0, :]
    y = data[:, 1, :]
    model.compile(optimizer='adam', loss='kl_divergence', metrics=['accuracy'])
    model.fit(x, y, epochs=5)
    print(model.predict(np.array([[2, 1]])))

