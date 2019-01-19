from database import Database
from werkzeug.security import generate_password_hash, check_password_hash


def email_exists(email):
    """(str) -> bool
    Returns True iff the email exists in the `users` table under `email` column
    """
    db = Database()
    q = """SELECT `email` FROM `users` WHERE `email` = %s"""
    db.cur.execute(q, email)

    exists = db.cur.fetchone() is not None
    db.con.close()
    return exists


def sign_up(email, password):
    """(str, str) -> NoneType
    Signs up a user with the given username and password
    """
    db = Database()
    q = """INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"""
    db.cur.execute(q, (email, generate_password_hash(password)))
    db.con.close()


def login(email, password):
    """(str, str) -> bool
    Returns True iff the given credentials match an account
    """
    db = Database()
    q = """SELECT `password` FROM `users` WHERE `email` = %s"""
    rows = db.cur.execute(q, email)
    if rows == 0:
        return False
    res = db.cur.fetchone()
    db.con.close()
    return check_password_hash(res['password'], password)


def fetch_user_from_id(user_id):
    """(int) -> dict of str:obj
    Returns the User object from the database with the given id
    """
    db = Database()
    q = """SELECT * FROM `users` WHERE `id` = %s"""
    db.cur.execute(q, user_id)
    user = db.cur.fetchone()
    db.con.close()
    return user


def fetch_user_from_email(email):
    """(str) -> dict of str:obj
    Returns the User object from the database with the given email
    """
    db = Database()
    q = """SELECT * FROM `users` WHERE `email` = %s"""
    db.cur.execute(q, email)
    user = db.cur.fetchone()
    db.con.close()
    return user
