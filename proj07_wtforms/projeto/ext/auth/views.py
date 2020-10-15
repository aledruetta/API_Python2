from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_login import login_user

from .models import User

bp = Blueprint("auth", __name__)


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        login_user(user)
        return redirect(url_for("site.index"))
    return render_template("login.html", form=form)


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    pass


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    pass
