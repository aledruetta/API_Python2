from flask import redirect, url_for, request
from flask_login import current_user, login_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from projeto.ext.auth import UserAuth
from projeto.ext.api.models import Estacao, Sensor
from projeto.ext.db import db


class AdminView(ModelView):
    @login_required
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("auth.login", next=request.url))


admin = Admin(name='flaskapi', template_mode='bootstrap3')

admin.add_view(AdminView(UserAuth, db.session))
admin.add_view(AdminView(Estacao, db.session))
admin.add_view(AdminView(Sensor, db.session))


def init_app(app):
    admin.init_app(app)
