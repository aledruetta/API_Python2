from flask_admin import Admin

from projeto.ext.admin.views import EstacaoView, SensorView, UserView
from projeto.ext.api.models import Estacao, Sensor
from projeto.ext.auth import UserAuth
from projeto.ext.db import db

admin = Admin(name='FlaskAPI', template_mode='bootstrap3')


def init_app(app):
    admin.add_view(EstacaoView(Estacao, db.session))
    admin.add_view(SensorView(Sensor, db.session))
    admin.add_view(UserView(UserAuth, db.session))

    admin.init_app(app)
