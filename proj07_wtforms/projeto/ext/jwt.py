from flask_jwt import JWT
from werkzeug.security import safe_str_cmp

from .auth.models import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and safe_str_cmp(user.password.encode("utf-8"),
                             password.encode("utf-8")):
        return user


def identity(payload):
    user_id = payload["identity"]
    return User.query.get(user_id)


def init_app(app):
    jwt = JWT(app, authenticate, identity)
