import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"), verbose=True)


class BaseConfig:
    """Base configs"""

    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATE_FOLDER = "templates"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_USERNAME_KEY = "email"
    JWT_AUTH_URL_RULE = "/token"
    JWT_EXPIRATION_DELTA = timedelta(seconds=86400)  # one day
    FLASK_ADMIN_SWATCH = "sandstone"


class ProdConfig(BaseConfig):
    """Production configs"""

    FLASK_ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI")


class DevConfig(BaseConfig):
    """Development configs"""

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")
