from flask import Flask, request, render_template,  jsonify
# from flask_session import Session
from gevent.pywsgi import WSGIServer
from calculate_result import calculate_result
from PyPDF2 import PdfReader
from analyze_text_internal import analyze_text_internal
import requests

app = Flask(__name__)

# app.config (Flask)
# app.config['LANGUAGES'] = ['ru']
# app.config['BABEL_DEFAULT_LOCALE'] = 'ru'

# print(app.config)
# create a session for storing text of resume 
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)





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

@app.route('/the_worst_result')
def the_worst_result():
    return render_template('the_worst_result.html')

@app.route('/bad_result')
def bad_result():
    return render_template('bad_result.html')

@app.route('/normal_result')
def normal_result():
    return render_template('normal_result.html')

@app.route('/good_result')
def good_result():
    return render_template('good_result.html')
    
@app.route('/excellent_result')
def excellent_result():
    return render_template('excellent_result.html')

@app.route('/main_ai')
def main_ai():
    return render_template('main_ai.html')

@app.route('/about_project')
def about_project():
    return render_template('about_project.html')

@app.route('/get_pdf', methods=['GET', 'POST'])
def get_pdf():
    if request.method == 'POST':
        file = request.files['pdf-file']
        pdf = PdfReader(file)
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        result = analyze_text_internal(text)
        result = int(result * 100)
        return render_template('main_ai.html', text=text, result=result)
    return render_template('main_ai.html')



if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    # app.run(debug=True)

