from flask import Flask, request, render_template, jsonify, redirect, url_for, session, abort, g, flash
# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from gevent.pywsgi import WSGIServer
from PyPDF2 import PdfReader
from analyze_text_internal import analyze_text_internal
import requests
from forms import RegistrationForm
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
import os
import sqlite3 
from FDataBase import FDataBase
from docx import Document
import docx
# from vk_auth import get_auth_url, get_access_token, get_user_data
# import vk_auth


# from forms import LoginForm

DATABASE = '/dss.db'
DEBUG = True 
SECRET_KEY = '95560364da6bde9581bc94dff5c97b235fcae17b'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'dss.db')))
app.config['SECRET_KEY'] = '95560364da6bde9581bc94dff5c97b235fcae17b'
app.config['PROPAGATE_EXCEPTIONS'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # создайте базу данных в текущей директории
# db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


# client_id = '52091976'
# client_secret = 'e5EbLZzbqsnqwFfKHsIt'

# auth_url = f'https://oauth.vk.com/authorize?client_id={client_id}&display=page&redirect_uri=https://decisionss.ru/callback&scope=email&response_type=code'
# logging.basicConfig(filename='error.log', level=logging.ERROR)


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row 
    return conn

def create_db():
    # вспомогательная функция для создания таблиц БД
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    # соединение с БД, если оно еще не установлено
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    # Закрываем соединение с БД, если оно было установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()

dbase = None 
@app.before_request
def before_request():
    # устанавливаем соединение с БД перед выполнением запроса
    global dbase 
    db = get_db()
    dbase = FDataBase(db)

@app.route('/')
def index():
    return render_template('title_list.html')


# @app.route('/recomendations', methods=['GET'])
# def recomendations():
#     result = int(request.args.get('result')) 
#     if not result:
#         return render_template('errorpage.html', num1 = 5, num2 = 0, num3 = 0, message="Нельзя посмотреть рекомендации, не загрузив резюме. Или другая ошибка"), 500
#     if 80 <= result and result <= 100:
#         return render_template('excellent_result.html', result=result)
#     elif 60 <= result and result < 80:
#         return render_template('good_result.html', result=result)
#     elif 40 <= result and result < 60:
#         return render_template('normal_result.html', result=result)
#     elif 20 <= result and result < 60:
#         return render_template('bad_result.html', result=result)
#     elif 0 <= result and result < 20:
#         return render_template('the_worst_result.html', result=result)
#     else:
#         return render_template('errorpage.html', num1 = 4, num2 = 0, num3 = 4), 404




# @app.route('/calculate', methods=['POST'])
# def calculate():
#     data = request.form['data']
#     data2 = request.form['data2']
#     data3 = request.form['data3']
#     data4 = request.form['data4']
#     data5 = request.form['data5']
#     data6 = request.form['data6']
#     # Perform your calculations with the data
#     result = calculate_result(data, data2, data3, data4, data5, data6)
#     return result

@app.route('/main_ai')
@login_required
def main_ai():
    return render_template('main_ai.html', name=current_user.get_username())

@app.route('/about_project')
def about_project():
    return render_template('about_project.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/get_pdf', methods=['GET', 'POST'])
def get_pdf():
    try:
        if request.method == 'POST':
            file = request.files['pdf-file']
            filename, file_extension = os.path.splitext(file.filename)

            if file_extension == '.pdf':
                pdf = PdfReader(file)
                text = ''
                for page in pdf.pages:
                    text += page.extract_text()
            elif file_extension in ['.docx']:
                doc = Document(file)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            elif file_extension == '.txt':
                text = file.read().decode('utf-8')
            else:
                return render_template('errorpage.html', num1 = 4, num2 = 0, num3 = 4), 404

            result = analyze_text_internal(text)
            result = int(result * 100)

            if not result:
                return render_template('errorpage.html', num1 = 5, num2 = 0, num3 = 0, message="Нельзя посмотреть рекомендации, не загрузив резюме. Или другая ошибка"), 500
            if 80 <= result and result <= 100:
                return render_template('excellent_result.html', result=result, text=text)
            elif 60 <= result and result < 80:
                return render_template('good_result.html', result=result, text=text)
            elif 40 <= result and result < 60:
                return render_template('normal_result.html', result=result, text=text)
            elif 20 <= result and result < 60:
                return render_template('bad_result.html', result=result, text=text)
            elif 0 <= result and result < 20:
                return render_template('the_worst_result.html', result=result, text=text)
            else:
                return render_template('errorpage.html', num1 = 4, num2 = 0, num3 = 4), 404

            # return render_template('main_ai.html', text=text, result=result,  name=current_user.get_username())
        return render_template('main_ai.html',  name=current_user.get_username())
    except:
        return render_template('errorpage.html', num1 = 5, num2 = 0, num3 = 0), 500


@app.route('/recomendations', methods=['GET'])
def recomendations():
    result = int(request.args.get('result')) 
    if not result:
        return render_template('errorpage.html', num1 = 5, num2 = 0, num3 = 0, message="Нельзя посмотреть рекомендации, не загрузив резюме. Или другая ошибка"), 500
    if 80 <= result and result <= 100:
        return render_template('excellent_result.html', result=result)
    elif 60 <= result and result < 80:
        return render_template('good_result.html', result=result)
    elif 40 <= result and result < 60:
        return render_template('normal_result.html', result=result)
    elif 20 <= result and result < 60:
        return render_template('bad_result.html', result=result)
    elif 0 <= result and result < 20:
        return render_template('the_worst_result.html', result=result)
    else:
        return render_template('errorpage.html', num1 = 4, num2 = 0, num3 = 4), 404


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data, password=form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    # form = LoginForm()
    # return render_template("login.html", title="Авторизация", form=form)
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            # return redirect(url_for('profile')) # улучшим жизнь людям
            return redirect(request.args.get("next") or url_for("profile"))
        flash("Неверная пара логин/пароль", "error")

    # vk_auth_url = get_auth_url()
    return render_template("login.html", title="Авторизация")

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['username']) > 4 and len(request.form['email']) > 9 and len(request.form['psw']) > 4:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['username'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")  
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД: ", "error")  
        else:
            flash("Неверно заполнены поля", "error") 
    return render_template('register.html', title="Регистрация")

# @app.route("/vk_login", methods=["GET"])
# def vk_login():
#     code = request.args.get("code")
#     access_token = get_access_token(code)
#     user_data = get_user_data(access_token)
#     # Create a new user or login existing user based on VK data
#     #...
#     return redirect(url_for("profile"))


# @app.route("/callback")
# def callback():
#     code = request.args.get("code")
#     if not code:
#         return "Error: missing code parameter", 400

#     access_token = vk_auth.get_access_token(code)
#     if not access_token:
#         return "Error: unable to obtain access token", 400

#     user_data = vk_auth.get_user_data(access_token)
#     if not user_data:
#         return "Error: unable to obtain user data", 400

    # Create a new user in your application's database
    # and log them in using Flask-Login
    # vk_username = user_data['first_name'] + ' ' + user_data['last_name']
    # vk_email = user_data['email']

    # user = dbase.get_user_by_email(vk_email)

    # if user:
    #     userlogin = UserLogin().create(user)
    #     login_user(userlogin, remember=True)
    #     flash("Вы успешно авторизованы", "success")
    #     return redirect(url_for('profile'))
    # else:
    #     res = dbase.addUser(vk_username, vk_email, access_token)
    #     if res:
    #         user = dbase.get_user_by_email(vk_email)
    #         userlogin = UserLogin().create(user)
    #         login_user(userlogin, remember=True)
    #         flash("Вы успешно зарегистрированы", "success")
    #         return redirect(url_for('profile'))
    #     else:
    #         flash("Ошибка при добавлении в БД", "error")
    #         return redirect(url_for('login'))



    # For example:
    #
    # user = User.query.filter_by(vk_id=user_data["id"]).first()
    # if user is None:
    #     user = User(vk_id=user_data["id"], name=user_data["first_name"], email=user_data["email"])
    #     db.session.add(user)
    #     db.session.commit()
    #
    # userlogin = UserLogin().create(user)
    # login_user(userlogin, remember=True)

    # return redirect(url_for("profile"))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', name=current_user.get_username(), email=current_user.get_email())
    # return f"""<p><a href="{url_for('logout')}">Выйти из профиля</a>
    # <p>user info: {current_user.get_id()}"""


@app.errorhandler(404)
def pagenotFound404(error):
    return render_template('errorpage.html', num1 = 4, num2 = 0, num3 = 4, message="Страница не найдена :("), 404




# @app.before_first_request
# def before_first_request():
#     print("before_first_request() called")

# @app.before_request
# def before_request():
#     print("before_request() called")

# @app.after_request
# def after_request(response):
#     print("after_request() called")
#     return response 

# @app.teardown_request
# def teardown_request(response):
#     print("teardown_request() called")
#     return response   

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  # создайте таблицы в базе данных
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    # app.run(debug=True)

