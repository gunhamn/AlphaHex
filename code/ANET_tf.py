
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

class ANET_tf(tf.keras.Model):
    def __init__(self, numInput=2, numOutput=2):
        super(ANET_tf, self).__init__()
        self.lossarray = []
        self.model = tf.keras.Sequential([
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(10, input_shape=(numInput,), activation='relu'),
            tf.keras.layers.Dense(15, activation='relu'),
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(numOutput, activation='softmax')
        ])
    def load(self, filepath):
        self.weights = self.load_weights(filepath=filepath)
        
    def forward(self, x, moves = None):
        x = np.array(x, dtype=np.float32)
        print(f'x: {x}')
        if x.ndim == 1:
            x = np.expand_dims(x, 0)
        logits = self.predict(x)
        print(f"predictions: {logits}")

        if moves!=None:
            set1 = set(moves)

            # Iterate over the indices of list2
            for i in range(len(logits)):
                # Check if the index+1 is in list1
                if i + 1 not in set1:
                    # If not, set the value to 0
                    logits[i] = 0
        logits = logits / np.sum(logits, axis=0, keepdims=True)
        print(f"logits: {logits}")
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
        data = np.array(data)
        x = data[:, 0, :]
        x = np.reshape(x, (-1, 2))
        y = data[:, 1, :]
        y = np.reshape(y, (-1, 2))
        print(f"Shape of x: {x.shape}")  # Debugging line
        print(f'x: {x}')
        print(f"Shape of y: {y.shape}")  # Debugging line
        print(f'y: {y}')
        history = self.fit(x, y, epochs=num_epochs, batch_size=batch_size, verbose=1)
        self.lossarray = history.history['loss']

    def plot(self):
        plt.plot(self.lossarray)
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title("Training Loss Over Epochs")
        plt.show()
    
    def save(self, path):
        self.model.save(path)



if __name__ == "__main__":
    net = ANET_tf()
    data = [[[1, 2], [0, 1]]]*2000
    # print(data)
    net.train(data)
    print(net.simpleForward(np.array([[1, 2]])))
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
    print(model.predict(np.array([[1, 2]])))

