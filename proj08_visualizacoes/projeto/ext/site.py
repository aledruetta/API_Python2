from flask import Blueprint, render_template
from flask_login import login_required

from .api.models import Estacao
from .auth.models import User

bp = Blueprint("site", __name__)


def init_app(app):
    app.register_blueprint(bp)


@bp.route("/")
def index():
    estacoes = Estacao.query.all()
    return render_template("index.html", title="Estações", estacoes=estacoes)


@bp.route("/protected")
@login_required
def protected():
    users = User.query.all()
    return render_template("protected.html", title="Secret", users=users)
