import requests
from flask import Flask, request, render_template, redirect, url_for, flash
from forms import cityField, SignupForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required, LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from decouple import config


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

@app.before_first_request
def create_tables():
    db.create_all()

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(crsf_enabled=False)
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations you are now registered!')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated():
    #     return redirect(url_for('weather'))
    form = LoginForm(crsf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('signup'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('weather')
        return redirect(next_page)
    
    return render_template('login.html', form=form)

        

@app.route("/weather", methods=['GET', 'POST'])
def weather():
    form = cityField(csrf_enabled=False)
    form_data = LoginForm(csrf_enabled=False)
    api_key = config('API_KEY')
    city = form.city.data

    url = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'.format(city=city, api_key=api_key)
    r = requests.get(url).json()

    user = User.query.filter_by(email=form_data.email.data).first()

    icon = r['weather'][0]['icon']
    icon_url = 'http://openweathermap.org/img/w/{}.png'
    icon_url_formatted = icon_url.format(icon)
    print(r)

    description = r['weather'][0]['main']
    temperature_decimals = r['main']['temp'] - 273.15
    temperature = str(int(round(temperature_decimals, 0))) + "°C"

    print(temperature)
    print(description)

    return render_template('weather.html', form=form, description=description, temperature=temperature, icon_url_formatted=icon_url_formatted, user=user)