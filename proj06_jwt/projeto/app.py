from flask import Flask
from flask_jwt import JWT

from projeto.ext import api, db
from projeto.ext.security import authenticate, identity


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super-secret-key"
    app.config["JWT_AUTH_USERNAME_KEY"] = "email"

    db.init_app(app)
    api.init_app(app)

    jwt = JWT(app, authenticate, identity)

    return app
