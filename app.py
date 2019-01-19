from flask import Flask, render_template
import functions.basic_functions as bf
import datetime

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()
