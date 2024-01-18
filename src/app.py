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
    # Perform your calculations with the data
    result = calculate_result(data)
    return result

def calculate_result(data):
    # Perform your calculations here
    # For demonstration purposes, let's just double the number
    try:
        return str(2 * int(data))
    except ValueError:
        return "Invalid input, please enter a number."

# if __name__ == '__main__':
#     app.run()

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    # app.run(debug=True)