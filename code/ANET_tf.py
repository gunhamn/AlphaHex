
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Conv1D, Add, ReLU, Dense, Flatten

""" Couldn't get imports to work.....
import tensorflow as tf
import torch
import torch.nn as nn
"""

class ANET_tf(tf.keras.Model):
    def __init__(self, numInput=(49, 3),
                 numOutput=49,
                 optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                 layers=None):
        super(ANET_tf, self).__init__()
        self.numInput = numInput
        self.lossarray = []
        self.optimizer = optimizer
        layers = layers if layers is not None else [
            Conv1D(64, 3, padding='same', input_shape=self.numInput),
            Conv1D(64, 3, padding='same'),
            ReLU(),
            Flatten(),
            tf.keras.layers.Dense(numOutput, activation='softmax')
        ]
        self.model = tf.keras.Sequential(layers)
    
    def load(self, filepath):
        self.weights = self.load_weights(filepath=filepath)
        
    def forward(self, x, moves = None):
        x = np.array(x, dtype=np.float32)
        # print(f'x: {x}')
        if x.ndim == 2:
            x = np.expand_dims(x, 0)
        #print(f'x: {x}')
        logits = self.predict(x, verbose=False)
        #print(f"predictions: {logits}, shape: {np.shape(logits)}")
        #print(f"moves: {moves}")

        if moves!=None:
            set1 = set(moves)

            # Iterate over the indices of list2
            for i in range(len(logits[0])):
                # Check if the index+1 is in list1
                if i not in set1:
                    # If not, set the value to 0
                    logits[0][i] = 0
            #print(f"logits before norm: {logits}")
            logits[0] = logits[0] / np.sum(logits[0], axis=0, keepdims=True)
        #print(f"logits: {logits}")
        return logits
    
    def call(self, inputs):
        return self.model(inputs)

    def simpleForward(self, x):
        x = np.array(x, dtype=np.float32)
        if x.ndim == 1:
            x = np.expand_dims(x, 0)
        return self.predict(x)

    def train(self, data, batch_size=10, num_epochs=50, learning_rate=0.001):
        
        self.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                     loss='kl_divergence',  # Assuming label encoding
                     metrics=['accuracy'])
        print(f"data: {data}")
        case = np.array([item[0] for item in data])
        target = np.array([item[1] for item in data])
        x=case
        y=target
        #data = np.array(data)
        #x = data[:, 0, :]
        #x = np.reshape(x, (-1, 2))
        #y = data[:, 1, :]
        #y = np.reshape(y, (-1, 2))
        """print(f"Shape of x: {x.shape}")  # Debugging line
        print(f'x: {x}')
        print(f"Shape of y: {y.shape}")  # Debugging line
        print(f'y: {y}')"""
        history = self.fit(x, y, epochs=num_epochs, batch_size=batch_size, verbose=1)
        self.lossarray.append(history.history['loss'])

    def plot(self):
        plt.plot(self.lossarray[0])
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title("Training Loss Over Epochs")
        plt.show()
    
    def save(self, path):
        self.model.save(path)

    def load_data(self, path='data_5game_1500sim.txt'):
        data = [[], []]
        with open(path, 'r') as file:
            for line in file:
                data[0].append(eval(line)[0])
                data[1].append(eval(line)[1])
        return data
    
    def process_data(self, data):
        # Takes in data on the format [[state], [distribution]]
        # meaning shape: [[1 + n*n], [n*n]
        # Outputs x = [player1pieces, player2pieces, playerTurn], y = [distribution]
        # on the format x.shape = (n*n*3), y.shape = (n*n)
        # where p1 -> playerTurn = 0, p2 -> playerTurn = 1
        x = [[], [], []]
        y = data[1].copy()
        for i in range(len(data[0])):
            if data[0][i][0] == 1:
                x[2].append([0]*len(data[1][0])) # 0 for player 1
            else:
                x[2].append([1]*len(data[1][0])) # 1 for player 2
        for i in range(len(data[0])):
            x[0].append([1 if data[0][i][j] == 1 else 0 for j in range(len(data[0][0]))])
            x[1].append([1 if data[0][i][j] == 2 else 0 for j in range(len(data[0][0]))])
        for i in range(len(data[0])): # Remove the first element, indicating player turn
            x[0][i].pop(0)
            x[1][i].pop(0)
        x = np.array(x)
        x = np.transpose(x, (1, 2, 0))
        y = np.array(y)
        return x, y

if __name__ == "__main__":
    model = ANET_tf()
    # Model summary to check the architecture
    model.build(input_shape=(None, *model.numInput))
    data = ANET_tf().load_data(path='data_5game_1500sim.txt')
    x, y = ANET_tf().process_data(data)
    print(f"x.shape: {x.shape}")
    print(f"y.shape: {y.shape}")
    
    model.train(data=list(zip(x, y)), num_epochs=40)
    #model.plot()

    data_verification = ANET_tf().load_data(path='data_1game_1500sim.txt')
    x_verification, y_verification = ANET_tf().process_data(data_verification)
    print(f"x_verification.shape: {x_verification.shape}")
    print(f"y_verification.shape: {y_verification.shape}")
    print(f'x_verification[-1].shape: {x_verification[-1].shape}')
    
    
    prediction = model.forward(x_verification[-1])
    print(f"prediction: {model.forward(x_verification[-1])}")
    # print the index of the highest value in the prediction
    print(f"Index of highest value in prediction: {np.argmax(prediction)}")
    print(f"y_verification[-1]: {y_verification[-1]}")
    print(f"Index of highest value in y_verification: {np.argmax(y_verification[-1])}")
    for i in range(len(y_verification)):
        prediction = model.forward(x_verification[i])
        print(f"Index of highest value in prediction: {np.argmax(prediction)}")
        print(f"Index of highest value in y_verification: {np.argmax(y_verification[i])}")
        
        
    #model.save('firstModel.keras')
