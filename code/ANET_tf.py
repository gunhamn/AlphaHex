
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Conv1D, Add, ReLU, Dense, Flatten
from CONFIG import CONFIG

class ANET_tf(tf.keras.Model):
    def __init__(self, numInput=CONFIG.get('numInput'),
                 numOutput=CONFIG.get('numOutput'),
                 optimizer=CONFIG.get('optimizer'),
                 learning_rate=CONFIG.get('learningRate'),
                 layers=CONFIG.get('layers')):
        super(ANET_tf, self).__init__()
        self.numInput = numInput
        self.lossarray = []
        if isinstance(optimizer, str):
            if optimizer.lower() == 'adam':
                self.optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
            elif optimizer.lower() == 'rmsprop':
                self.optimizer = tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
            elif optimizer.lower() == 'adagrad':
                self.optimizer = tf.keras.optimizers.Adagrad(learning_rate=learning_rate)
            elif optimizer.lower() == 'adamax':
                self.optimizer = tf.keras.optimizers.Adamax(learning_rate=learning_rate)
            elif optimizer.lower() == 'nadam':
                self.optimizer = tf.keras.optimizers.Nadam(learning_rate=learning_rate)
            else: #default optimizer
                self.optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        if layers is not None:
            # Initialize layers from config
            layer_objs = []
            for layer in layers:
                if layer['type'] == 'Conv1D':
                    layer_objs.append(tf.keras.layers.Conv1D(filters=layer['filters'], kernel_size=layer['kernel_size'],
                                                            padding=layer['padding'], input_shape=layer.get('input_shape', None)))
                elif layer['type'] == 'ReLU':
                    layer_objs.append(tf.keras.layers.ReLU())
                elif layer['type'] == 'Flatten':
                    layer_objs.append(tf.keras.layers.Flatten())
                elif layer['type'] == 'tanH':
                    layer_objs.append(tf.keras.layers.Activation('tanh'))
                elif layer['type'] == 'softmax':
                    layer_objs.append(tf.keras.layers.Activation('softmax'))
                elif layer['type'] == 'sigmoid':
                    layer_objs.append(tf.keras.layers.Activation('sigmoid'))
                elif layer['type'] == 'Dense':
                    layer_objs.append(tf.keras.layers.Dense(units=layer['units'], activation=layer['activation']))
            self.model = tf.keras.Sequential(layer_objs)
        else:
            # Default architecture
            self.model = tf.keras.Sequential([
                tf.keras.layers.Conv1D(64, 3, padding='same', input_shape=self.numInput),
                tf.keras.layers.Conv1D(64, 3, padding='same'),
                tf.keras.layers.ReLU(),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(numOutput, activation='softmax')
            ])
    
    def load(self, filepath):
        self.weights = self.load_weights(filepath=filepath)
        
    def forward(self, x, moves = None):
        x = self.process_state(x)
        x = np.array(x, dtype=np.float32)
        if x.ndim == 2:
            x = np.expand_dims(x, 0)
        logits = self.predict(x, verbose=False)
        if moves!=None:
            set1 = set(moves)
            # Iterate over the indices of list2
            for i in range(len(logits[0])):
                # Check if the index+1 is in list1
                if i not in set1:
                    # If not, set the value to 0
                    logits[0][i] = 0
            logits[0] = logits[0] / np.sum(logits[0], axis=0, keepdims=True)
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
                     loss='kl_divergence',
                     metrics=['accuracy'])
        x, y = self.process_data(data)
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
        
        data = self.correct_dims(data)
        x = [[], [], []]
        y = data[1].copy()
        for i in range(len(data[0])):
            if data[0][i][0] == 1:
                x[2].append([0]*(len(data[1][0]))) # 0 for player 1
            else:
                x[2].append([1]*(len(data[1][0]))) # 1 for player 2
        for row in data[0]:
            x[0].append([1 if value == 1 else 0 for value in row])
            x[1].append([1 if value == 2 else 0 for value in row])
        for i in range(len(data[0])): # Remove the first element, indicating player turn
            x[0][i].pop(0)
            x[1][i].pop(0)
        x = np.array(x)
        x = np.transpose(x, (1, 2, 0))
        y = np.array(y)
        return x, y
    
    def correct_dims(self, data):
        # Annoyingly long function to correct the dimensions of the data
        # Verify the current format by checking if the first element's length is 2
        if len(data[0]) == 2: # Initialize the corrected data format with the correct outer array sizes
            corrected_data = [[] for _ in range(2)]
            # Iterate over the original data to reorganize it
            for i in range(len(data)):
                for j in range(len(data[i])):
                    corrected_data[j].append(data[i][j])
            # Combining inner lists to form the correct innermost arrays
            new_corrected_data = []
            for group in corrected_data:
                new_group = []
                for sub_group in group:
                    new_sub_group = []
                    for element in sub_group:
                        if isinstance(element, list):
                            new_sub_group.extend(element)
                        else:
                            new_sub_group.append(element)
                    new_group.append(new_sub_group)
                new_corrected_data.append(new_group)
            return new_corrected_data
        else:
            return data
        
    def process_state(self, state):
        # Takes in data on the format [[state], [distribution]]
        # meaning shape: [[1 + n*n], [n*n]
        # Outputs x = [player1pieces, player2pieces, playerTurn], y = [distribution]
        # on the format x.shape = (n*n*3), y.shape = (n*n)
        # where p1 -> playerTurn = 0, p2 -> playerTurn = 1
        x = [[], [], []]
        data = state.copy()
        if data[0] == 1:
            x[2].extend([0]*(len(data)-1)) # 0 for player 1
        else:
            x[2].extend([1]*(len(data)-1)) # 1 for player 2
        data.pop(0)
        for i in range(len(data)):
            x[0].extend([1 if data[i] == 1 else 0])
            x[1].extend([1 if data[i] == 2 else 0])

        x = np.array(x)
        x = np.transpose(x, (1, 0))
        return x

if __name__ == "__main__":
    model = ANET_tf()
    # Model summary to check the architecture
    model.build(input_shape=(None, *model.numInput))
    data = ANET_tf().load_data(path='data_1game_1500sim.txt')
    model.train(data=data, batch_size=100, num_epochs=2)
    # model.plot()
    state = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    prediction = model.forward(state)
    print(f"Index of highest value in prediction: {np.argmax(prediction)}")
    #model.save('bigModel.keras')
    """
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
        
    """
