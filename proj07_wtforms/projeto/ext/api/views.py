from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from projeto.ext.db import db

from .models import Estacao, Sensor


class ApiEstacao(Resource):
    def get(self):
        estacoes = Estacao.query.all()
        data = [estacao.json() for estacao in estacoes]
        return {"resources": data}

    @jwt_required()
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


class ApiEstacaoId(Resource):
    def get(self, id):
        estacao = Estacao.query.get(id)

        if estacao:
            return {"resource": estacao.json()}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
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

        if estacao:
            db.session.delete(estacao)
            db.session.commit()

            return {"deleted": estacao.json()}
        return {"error": "Recurso inexistente!"}


class ApiSensor(Resource):
    def get(self):
        sensores = Sensor.query.all()
        data = [sensor.json() for sensor in sensores]
        return {"resources": data}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "tipo", type=str, required=True, help="Argumento requerido!"
        )
        parser.add_argument(
            "estacao_id", type=int, required=True, help="Argumento requerido!"
        )

        data = parser.parse_args()

        sensor = Sensor(
            tipo=data["tipo"],
            estacao_id=data["estacao_id"],
        )

        db.session.add(sensor)
        db.session.commit()

        return {"created": sensor.json()}


class ApiSensorId(Resource):
    def get(self, id):
        sensor = Sensor.query.get(id)

        if sensor:
            return {"resource": sensor.json()}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("tipo", type=str)

        data = parser.parse_args()
        sensor = Sensor.query.get(id)

        if sensor:
            sensor.tipo = data["tipo"] if data["tipo"] else sensor.tipo

            db.session.add(sensor)
            db.session.commit()

            return {"updated": sensor.json()}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
    def delete(self, id):
        sensor = Sensor.query.get(id)

        if sensor:
            db.session.delete(sensor)
            db.session.commit()

            return {"deleted": sensor.json()}
        return {"error": "Recurso inexistente!"}
