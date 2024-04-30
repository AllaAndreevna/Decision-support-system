import numpy as np
import math

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def calculate_result(data, data2, data3, data4, data5, data6):
    # Perform your calculations here
    # For demonstration purposes, let's just double the number
    try:
        # this is the simplest version of neural network which is called
        # perceptron

        training_inputs = np.array([[1,1,1,0,0,0],
                                    [1,1,1,1,0,1],
                                    [0,1,1,1,0,0],
                                    [1,0,0,0,1,1],
                                    [1,0,1,0,1,1]])

        training_outputs = np.array([[1,1,1,0,0]]).T

        np.random.seed(1)

        synaptic_weights = 2 * np.random.random((6,1)) - 1

        # now we will teach out neuronetwork!!

        for i in range(20000):
            input_layer = training_inputs
            outputs = sigmoid(np.dot(input_layer, synaptic_weights))

            err = training_outputs - outputs
            adjustments = np.dot(input_layer.T, err * (outputs*(1 - outputs)))

            synaptic_weights += adjustments

        #TEST!!!
        new_inputs = np.array([int(data), int(data2), int(data3), int(data4), int(data5), int(data6)])
        output = sigmoid(np.dot(new_inputs, synaptic_weights))

        return str(int(output*100))

    except ValueError:
        return "Invalid input, please enter a number."