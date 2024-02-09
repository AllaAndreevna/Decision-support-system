from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# var corsOptions = {
#   origin: "http://localhost:3000"
# };

# app.use(cors(corsOptions));

@app.route('/')
def index():
    return render_template('title_list.html')

@app.route('/main')
def main_page():
    return render_template('main_page.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.form['data']
    data2 = request.form['data2']
    data3 = request.form['data3']
    data4 = request.form['data4']
    data5 = request.form['data5']
    data6 = request.form['data6']
    # Perform your calculations with the data
    result = calculate_result(data, data2, data3, data4, data5, data6)
    return result

def calculate_result(data, data2, data3, data4, data5, data6):
    # Perform your calculations here
    # For demonstration purposes, let's just double the number
    try:

        # this is the simplest version of neural network which is called
        # perceptron
        import numpy as np

        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        training_inputs = np.array([[1,0,1,0,0,0],
                                    [1,1,1,1,1,1],
                                    [1,0,0,1,0,1],
                                    [0,1,1,0,1,0],
                                    [1,0,1,0,0,1]])


        training_outputs = np.array([[1,1,0,0,0]]).T

        np.random.seed(1)

        synaptic_weights = 2 * np.random.random((6,1)) - 1

        #print("Случайные инициализирующие веса:")
        #print(synaptic_weights)

        # now we will teach out neuronetwork!!

        for i in range(20000):
            input_layer = training_inputs
            outputs = sigmoid(np.dot(input_layer, synaptic_weights))

            err = training_outputs - outputs
            adjustments = np.dot(input_layer.T, err * (outputs*(1 - outputs)))

            synaptic_weights += adjustments

        #print("Веса после обучения")
        #print(synaptic_weights)

        #print("Результат после обучения")
        #print(outputs)

        #TEST!!!
        #new_inputs = np.array([1, 0, 0, 1, 0, 1])  # Новая ситуация
        new_inputs = np.array([int(data), int(data2), int(data3), int(data4), int(data5), int(data6)])
        output = sigmoid(np.dot(new_inputs, synaptic_weights))

        #print("Новая ситуация")
        #print(output)

        #return str(int(data) + int(data2) + int(data3)+ int(data4)+ int(data5)+ int(data6))
        return str(output)

    except ValueError:
        return "Invalid input, please enter a number."

# if __name__ == '__main__':
#     app.run()

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    # app.run(debug=True)