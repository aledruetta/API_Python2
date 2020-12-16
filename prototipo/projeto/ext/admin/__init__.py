from flask_admin import Admin
from projeto.ext.admin.views import EstacaoView, SensorView, SensorTipoView, UserView
from projeto.ext.api.models import Estacao, Sensor, SensorTipo
from projeto.ext.auth.models import UserAuth
from projeto.ext.db import db

admin = Admin(name="Dashboard", template_mode="bootstrap3")


def init_app(app):
    admin.init_app(app)
    views = [
        UserView(UserAuth, db.session),
        EstacaoView(Estacao, db.session),
        SensorTipoView(SensorTipo, db.session),
        SensorView(Sensor, db.session),
    ]
    admin.add_views(*views)
