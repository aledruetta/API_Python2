from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

from .api.models import Estacao

bp = Blueprint("site", __name__)


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


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


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("site.index"))
    return render_template("login.html", form=form)
