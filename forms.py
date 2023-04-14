from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf import FlaskForm

class cityField(FlaskForm):
    city = StringField('Enter a City', validators=[DataRequired()])
    submit = SubmitField('Search')

class SignupForm(FlaskForm):
    email = StringField('Enter an email', validators=[DataRequired()])
    password = PasswordField('Enter a password', validators=[DataRequired()])
    password2 = PasswordField('Enter password again', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

class LoginForm(FlaskForm):
    email = StringField('Enter an email', validators=[DataRequired()])
    password = PasswordField('Enter a password', validators=[DataRequired()])
    submit = SubmitField('Login')

