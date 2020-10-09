from flask import Blueprint, request
from flask_restful import Resource

from projeto.ext.db import db
from .models import Estacao

bp = Blueprint("api", __name__)


class ApiRest(Resource):
    def get(self):
        estacoes = Estacao.query.all()
        data = [estacao.json() for estacao in estacoes]
        return {"resources": data}

    def post(self):
        data = request.get_json()

        estacao = Estacao(
            local=data["local"],
            latitude=data["latitude"],
            longitude=data["longitude"],
        )

        db.session.add(estacao)
        db.session.commit()

        return {"created": estacao.json()}


class ApiRestId(Resource):
    def get(self, id):
        estacao = Estacao.query.get(id)

        if estacao:
            return {"resource": estacao.json()}
        return {"error": "Recurso inexistente!"}

    def put(self, id):
        data = request.get_json()
        estacao = Estacao.query.get(id)

        if estacao:
            estacao.local = data.get("local", estacao.local)
            estacao.latitude = data.get("latitude", estacao.latitude)
            estacao.longitude = data.get("longitude", estacao.longitude)

            db.session.add(estacao)
            db.session.commit()

            return {"updated": estacao.json()}
        return {"error": "Recurso inexistente!"}

    def delete(self, id):
        estacao = Estacao.query.get(id)

        if estacao:
            db.session.delete(estacao)
            db.session.commit()

            return {"deleted": estacao.json()}
        return {"error": "Recurso inexistente!"}
