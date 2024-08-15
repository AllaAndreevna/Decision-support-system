from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# class LoginForm(FlaskForm):
#     email = StringField("Почта: ", validators=[Email()])
#     psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=5, max=50)])
#     remember = BooleanField("Запомнить", default=False)
#     submit = SubmitField("Войти")