from flask import Flask

from .ext import auth, api, db, jwt, site


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super-secret-key"
    app.config["JWT_AUTH_USERNAME_KEY"] = "email"
    app.config["JWT_AUTH_URL_RULE"] = "/token"

    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    auth.init_app(app)
    site.init_app(app)

    return app
