import flask_login as log
import functions.basic_functions as bf
import functions.database_ops as db
import datetime
import smartcar
import os
from flask import Flask, redirect, request, jsonify, render_template, url_for
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.urandom(16)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id='8af861e3-570a-45f5-b321-ef755778ff42',
    client_secret='5347869a-217b-4775-ae3e-c5ed66380c82',
    redirect_uri='http://localhost:5000/smartcar/exchange',
    scope=['read_vehicle_info'],
    test_mode=True
)
login_manager = log.LoginManager()
login_manager.init_app(app)


""" LOGIN """


@login_manager.user_loader
def load_user(user_id):
    user = db.fetch_user_from_id(int(user_id))
    return User(user['id'], user['email'])


class User(log.UserMixin):
    def __init__(self, usr_id, email):
        self.id = int(usr_id)
        self.email = email


""" FLASK APP """


@app.route('/')
def home():
    """ The Home Page """
    return render_template("home.html", user=log.current_user)


@app.route('/settings')
def settings():
    """ The Settings Page """
    years = bf.get_next_x_years(datetime.datetime.now().year, 10)
    return render_template("settings.html", years=years, user=log.current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    """ The Log In Page """
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('pass')
        login_success = db.login(email, password)
        if not login_success:
            return render_template("login.html", err=True, user=log.current_user)
        else:
            user = db.fetch_user_from_email(email)
            log.login_user(User(user['id'], user['email']))
            return redirect(url_for('home'))
    return render_template("login.html", err=False, user=log.current_user)


@app.route('/logout')
@log.login_required
def logout():
    log.logout_user()
    return redirect(url_for('home'))


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """ The Sign Up Page """
    if request.method == "POST":
        # Catch any errors with form
        email_exists = db.email_exists(request.form.get('email'))
        pass_match = bf.pass_match(request.form.get('pass'), request.form.get('rePass'))
        if email_exists or not pass_match:
            return render_template("signup.html", email=email_exists, pass_match=pass_match, user=log.current_user)
        else:
            db.sign_up(request.form.get('email'), request.form.get('pass'))
            return redirect(url_for('login'))
    return render_template("signup.html", email=False, pass_match=True, user=log.current_user)


@app.route('/borrow')
def borrow():
    """The borrow a car page"""
    return render_template("borrow.html", user=log.current_user)


@app.route('/smarcar/login', methods=['GET'])
def smart_login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/smartcar/exchange', methods=['GET'])
def smart_exchange():
    code = request.args.get('code')

    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return '', 200


@app.route('/smartcar/vehicle', methods=['GET'])
def smart_vehicle():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    info = vehicle.info()
    print(info)

    return jsonify(info)


if __name__ == '__main__':
    app.run(port=5000)

