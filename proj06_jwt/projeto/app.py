from flask import Flask
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp

from projeto.ext import api, db
# from projeto.ext.api.models import User


class User:
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


users = [
    User(1, "alvaro", "123456"),
    User(2, "alejandro", "123456"),
]

username_table = {u.email: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(email, password):
    print(email, password)
    user = username_table.get(email, None)
    if user and safe_str_cmp(
        user.password, password
    ):
        return user


def identity(payload):
    user_id = payload["identity"]
    return user_id.get(user_id, None)


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super-secret-key"

    db.init_app(app)
    api.init_app(app)

    jwt = JWT(app, authenticate, identity)

    return app
