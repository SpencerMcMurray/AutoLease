import flask_login as log
import basic_functions as bf
import database_ops as db
import datetime
import smartcar
import os
from flask import Flask, redirect, request, jsonify, render_template, url_for, session
from flask_cors import CORS
from moneyRequests import sendMoneyRequestOneTimeContact

app = Flask(__name__)
app.secret_key = os.urandom(16)
CORS(app)
# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id='8af861e3-570a-45f5-b321-ef755778ff42',
    client_secret='bacddc7a-d359-46de-a56d-d6f5c338edc5',
    redirect_uri='http://localhost:5000/smartcar/exchange',
    scope=['read_vehicle_info', 'control_security', 'read_odometer', 'read_location'],
    test_mode=False
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


@app.before_request
def make_session_permanent():
    session.permanent = True


""" FLASK APP """


@app.route('/')
def home():
    """ The Home Page """
    return render_template("home.html", user=log.current_user)


@app.route('/settings')
@log.login_required
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
            return redirect(url_for('account'))
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


@app.route('/account', methods=["GET", "POST"])
@log.login_required
def account():
    """ The My Account Page """
    lend_id = -1
    if request.method == "POST":
        lend_id = request.form.get('id')
        session['lend'] = lend_id
        print(lend_id)
    borrows = db.get_my_borrows(log.current_user.id)
    lendings = db.get_my_lendings(log.current_user.id)
    return render_template("account.html", user=log.current_user, borrows=borrows, lendings=lendings, lend_id=lend_id)


@app.route('/borrow', methods=["GET", "POST"])
def borrow():
    """The borrow a car page"""
    if request.method == "POST":
        print(request.form.get('total-in'))
        # Ugly, but that's life.
        money_url = sendMoneyRequestOneTimeContact('b51e7f6a-18ef-473d-afe7-b5abbd026d9c',
                                                   'CA1TAuUG9Ned35wF', 'requestID',
                                                   'deviceID', 'CA1ARFrD8x2J5U94', '2019-01-18T16:12:12.000Z',
                                                   '2019-01-20T16:12:12.000Z', int(request.form.get('total-in')))
        session['model'] = request.form.get('model')
        session['time'] = request.form.get('time')
        db.assign_borrow(log.current_user.id,
                         (datetime.datetime.now() + datetime.timedelta(days=int(session['time']))).strftime("%Y-%m-%d"),
                         session['model'], 1)
        return render_template("borrow.html", user=log.current_user, money_url=money_url)
    return render_template("borrow.html", user=log.current_user, money_url=None)


@app.route('/smartcar/login', methods=['GET'])
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
    return redirect(url_for('smart_unlock'))


@app.route('/smartcar/vehicles', methods=['GET'])
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


@app.route('/smartcar/unlock', methods=['GET'])
def smart_unlock():
    global access
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    print(vehicle)
    vehicle.unlock()
    global locked
    locked = 0
    return redirect(url_for('confirm'))


@app.route('/smartcar/confirm')
def confirm():
    """ The Page for confirming that the car has been lock/unlocked """
    return render_template("confirm_unlock.html", locked=locked, user=log.current_user)


@app.route('/smartcar/odom', methods=['GET'])
def read_odom():
    global access
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    response = vehicle.odometer()
    print(response)
    print(response["data"]["distance"])
    return ""


@app.route('/smartcar/local', methods=['GET'])
def get_local():
    global access
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    response = vehicle.location()
    print(response)
    return ""


if __name__ == '__main__':
    app.run(port=5000, debug=True)

