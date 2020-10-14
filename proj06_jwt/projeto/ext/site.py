from flask import Blueprint, render_template

from .api.models import Estacao

bp = Blueprint("site", __name__)


def init_app(app):
    app.register_blueprint(bp)


@bp.route("/")
def index():
    estacoes = Estacao.query.all()
    return render_template(
        "index.html",
        title="Estações",
        estacoes=estacoes
    )
