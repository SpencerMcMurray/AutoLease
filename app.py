import functions.basic_functions as bf
import datetime
import smartcar
from flask import Flask, redirect, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id='8af861e3-570a-45f5-b321-ef755778ff42',
    client_secret='5347869a-217b-4775-ae3e-c5ed66380c82',
    redirect_uri='http://localhost:5000/smartcar/exchange',
    scope=['read_vehicle_info', 'control_security', 'read_odometer'],
    test_mode=False
)


@app.route('/')
def home():
    """ The Home Page """
    return render_template("home.html")


@app.route('/settings')
def settings():
    """ The Settings Page """
    years = bf.get_next_x_years(datetime.datetime.now().year, 10)
    return render_template("settings.html", years=years)


@app.route('/login')
def login():
    """ The Log In Page """
    return render_template("login.html")


@app.route('/signup')
def signup():
    """ The Sign Up Page """
    return render_template("signup.html")

@app.route('/borrow')
def borrow():
    """The borrow a car page"""
    return render_template("borrow.html")


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
    return '', 200


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
    return ""
@app.route('/smartcar/lock', methods=['GET'])
def smart_lock():
    global access
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    print(vehicle)
    vehicle.lock()
    return ""

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

if __name__ == '__main__':
    app.run(port=5000)

