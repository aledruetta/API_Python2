from flask import Blueprint, request
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse

from projeto.ext.db import db

from .models import Estacao

bp = Blueprint("api", __name__)


class ApiRest(Resource):
    def get(self):
        estacoes = Estacao.query.all()
        data = [estacao.json() for estacao in estacoes]
        return {"resources": data}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "local", type=str, required=True, help="Argumento requerido!"
        )
        parser.add_argument(
            "latitude", type=str, required=True, help="Argumento requerido!"
        )
        parser.add_argument(
            "longitude", type=str, required=True, help="Argumento requerido!"
        )

        data = parser.parse_args()

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
        parser = reqparse.RequestParser()
        parser.add_argument("local", type=str)
        parser.add_argument("latitude", type=str)
        parser.add_argument("longitude", type=str)

        data = parser.parse_args()
        estacao = Estacao.query.get(id)

        if estacao:
            estacao.local = data["local"] if data["local"] else estacao.local
            estacao.latitude = (
                data["latitude"] if data["latitude"] else estacao.latitude
            )
            estacao.longitude = (
                data["longitude"] if data["longitude"] else estacao.longitude
            )

            db.session.add(estacao)
            db.session.commit()

            return {"updated": estacao.json()}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
    def delete(self, id):
        estacao = Estacao.query.get(id)
        print(current_identity)

        if estacao:
            db.session.delete(estacao)
            db.session.commit()

            return {"deleted": estacao.json()}
        return {"error": "Recurso inexistente!"}
