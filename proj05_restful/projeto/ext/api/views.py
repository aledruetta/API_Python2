from flask import Blueprint, request, render_template
from projeto.ext.db import db
from .models import Estacao

bp = Blueprint("api", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


# listar estacoes
@bp.route("/api")
def list():
    estacoes = Estacao.query.all()
    data = [estacao.json() for estacao in estacoes]
    return {"estacoes": data}


# apresentar uma estacao pelo id
@bp.route("/api/<int:id>")
def read(id):
    estacao = Estacao.query.get(id)
    return {"estacao": estacao.json()}


# criar estacao
@bp.route("/api", methods=["POST"])
def create():
    data = request.get_json()

    estacao = Estacao(
        local=data["local"],
        latitude=data["latitude"],
        longitude=data["longitude"],
    )

    db.session.add(estacao)
    db.session.commit()

    return {"msg": "Success!"}


# atualizar dados estacao pelo id
@bp.route("/api/<int:id>", methods=["POST"])
def update(id):
    data = request.get_json()
    estacao = Estacao.query.get(id)

    estacao.local = data.get("local", estacao.local)
    estacao.latitude = data.get("latitude", estacao.latitude)
    estacao.longitude = data.get("longitude", estacao.longitude)

    db.session.add(estacao)
    db.session.commit()

    return {"msg": estacao.json()}


# deletar estacao pelo id
@bp.route("/api/<int:id>/del", methods=["POST"])
def delete(id):
    estacao = Estacao.query.get(id)

    db.session.delete(estacao)
    db.session.commit()

    return {"msg": "Success!"}
