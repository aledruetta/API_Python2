from flask import redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required


class AdminView(ModelView):
    @login_required
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("auth.login", next=request.url))


class UserView(AdminView):
    column_list = ("id", "email", "is_admin")
    column_sortable_list = ()

    can_create = True
    can_delete = True
    can_edit = False


class EstacaoView(AdminView):
    column_list = ("id", "local", "latitude", "longitude", "created_on",
                   "updated_on")
    form_excluded_columns = ("created_on", "updated_on")
    column_sortable_list = ()


class SensorTipoView(AdminView):
    # column_list = ("id", "codigo", "descricao", "params")
    column_sortable_list = ()


class SensorView(AdminView):
    # column_list = ("id", "tipo", "estacao")
    column_sortable_list = ()

    form_excluded_columns = [
        "leituras",
    ]
