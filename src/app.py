from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
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

if __name__ == '__main__':
    app.run()

# if __name__ == '__main__':
#     app.run(debug=True)