from datetime import timedelta

from flask import Flask
from projeto.ext import admin, api, auth, db, jwt, site


def create_app():
    app = Flask(__name__)
    app.config.from_object("projeto.config.DevConfig")

    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    auth.init_app(app)
    admin.init_app(app)
    site.init_app(app)

    return app
