from datetime import datetime

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from projeto.ext.db import db

from .models import Estacao, Sensor, Leitura


class ApiEstacao(Resource):
    def get(self):
        estacoes = Estacao.query.all()
        data = [estacao.json() for estacao in estacoes]
        return {"resources": data}

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("local",
                            type=str,
                            required=True,
                            help="Argumento requerido!")
        parser.add_argument("latitude",
                            type=str,
                            required=True,
                            help="Argumento requerido!")
        parser.add_argument("longitude",
                            type=str,
                            required=True,
                            help="Argumento requerido!")

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
    def get(self, estacao_id):
        estacao = Estacao.query.get(estacao_id)

        if estacao:
            return {"resource": estacao.json()}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
    def put(self, estacao_id):
        parser = reqparse.RequestParser()
        parser.add_argument("local", type=str)
        parser.add_argument("latitude", type=str)
        parser.add_argument("longitude", type=str)

        data = parser.parse_args()
        estacao = Estacao.query.get(estacao_id)

        if estacao:
            estacao.local = data["local"] if data["local"] else estacao.local
            estacao.latitude = (data["latitude"]
                                if data["latitude"] else estacao.latitude)
            estacao.longitude = (data["longitude"]
                                 if data["longitude"] else estacao.longitude)

            db.session.add(estacao)
            db.session.commit()

            return {"updated": estacao.json()}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
    def delete(self, estacao_id):
        estacao = Estacao.query.get(estacao_id)

        if estacao:
            db.session.delete(estacao)
            db.session.commit()

            return {"deleted": estacao.json()}
        return {"error": "Recurso inexistente!"}


class ApiEstacaoIdSensor(Resource):
    def get(self, estacao_id):
        estacao = Estacao.query.get(estacao_id)
        if estacao:
            sensores = estacao.sensores
            data = [sensor.json() for sensor in sensores]
            return {"resources": data}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
    def post(self, estacao_id):
        parser = reqparse.RequestParser()
        parser.add_argument("tipo",
                            type=str,
                            required=True,
                            help="Argumento requerido!")
        parser.add_argument("descricao",
                            type=str,
                            required=True,
                            help="Argumento requerido!")
        parser.add_argument("params",
                            type=str,
                            required=True,
                            help="Argumento requerido!")

        data = parser.parse_args()

        sensor = Sensor(tipo=data["tipo"],
                        descricao=data["descricao"],
                        params=data["params"],
                        estacao_id=estacao_id)

        db.session.add(sensor)
        db.session.commit()

        return {"created": sensor.json()}


class ApiEstacaoIdSensorId(Resource):
    def get(self, estacao_id, sensor_id):
        estacao = Estacao.query.get(estacao_id)
        if estacao:
            sensor = estacao.get_sensor(sensor_id)
            return {"resource": sensor.json()}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
    def put(self, estacao_id, sensor_id):
        parser = reqparse.RequestParser()
        parser.add_argument("tipo", type=str)
        parser.add_argument("descricao", type=str)
        parser.add_argument("params", type=str)

        data = parser.parse_args()
        estacao = Estacao.query.get(sensor_id)

        if estacao:
            sensor = estacao.get_sensor(sensor_id)
            sensor.tipo = data["tipo"] if data["tipo"] else sensor.tipo
            sensor.descricao = (data["descricao"]
                                if data["descricao"] else sensor.descricao)
            sensor.params = (data["params"]
                                 if data["params"] else sensor.params)

            db.session.add(sensor)
            db.session.commit()

            return {"updated": sensor.json()}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
    def delete(self, estacao_id, sensor_id):
        estacao = Estacao.query.get(sensor_id)

        if estacao:
            sensor = estacao.get_sensor(sensor_id)
            db.session.delete(sensor)
            db.session.commit()

            return {"deleted": sensor.json()}
        return {"error": "Recurso inexistente!"}


class ApiSensorIdParam(Resource):
    def get(self, sensor_id, param):
        sensor = Sensor.query.get(sensor_id)
        if sensor:
            leituras = [leitura.json() for leitura in sensor.leituras]
            return {"resource": leituras}
        return {"error": "Recurso inexistente!"}

    @jwt_required()
    def post(self, sensor_id, param):
        parser = reqparse.RequestParser()
        parser.add_argument("valor",
                            type=str,
                            required=True,
                            help="Argumento requerido!")
        parser.add_argument("datahora",
                            type=str,
                            required=True,
                            help="Argumento requerido!")

        data = parser.parse_args()

        datahora = datetime.fromtimestamp(int(data["datahora"]))

        leitura = Leitura(datahora=datahora,
                          valor=data["valor"],
                          param=param,
                          sensor_id=sensor_id)

        db.session.add(leitura)
        db.session.commit()

        return {"created": leitura.json()}
