from flask_jwt import JWT
from passlib.hash import sha256_crypt

from .auth.models import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and sha256_crypt.verify(password, user.password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return User.query.get(user_id)


def init_app(app):
    jwt = JWT(app, authenticate, identity)
