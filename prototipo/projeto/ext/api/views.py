from datetime import datetime

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from projeto.ext.api.models import Estacao, Leitura, Sensor
from projeto.ext.db import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

HTTP_RESPONSE_CREATED = 201
HTTP_RESPONSE_NOT_FOUND = 404


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
        return {"created": estacao.json()}, HTTP_RESPONSE_CREATED


class ApiEstacaoId(Resource):
    def get(self, estacao_id):
        try:
            estacao = Estacao.query.get(estacao_id)
            return {"resource": estacao.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND

    @jwt_required()
    def put(self, estacao_id):
        parser = reqparse.RequestParser()
        parser.add_argument("local", type=str)
        parser.add_argument("latitude", type=str)
        parser.add_argument("longitude", type=str)

        data = parser.parse_args()

        try:
            estacao = Estacao.query.get(estacao_id)

            estacao.local = data["local"] if data["local"] else estacao.local
            estacao.latitude = (data["latitude"]
                                if data["latitude"] else estacao.latitude)
            estacao.longitude = (data["longitude"]
                                 if data["longitude"] else estacao.longitude)

            db.session.add(estacao)
            db.session.commit()
            return {"updated": estacao.json()}

        except (AttributeError, IntegrityError):
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND

    @jwt_required()
    def delete(self, estacao_id):
        try:
            estacao = Estacao.query.get(estacao_id)
            db.session.delete(estacao)
            db.session.commit()
            return {"deleted": estacao.json()}

        except (IntegrityError, UnmappedInstanceError):
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND


class ApiEstacaoIdSensor(Resource):
    def get(self, estacao_id):
        try:
            estacao = Estacao.query.get(estacao_id)
            sensores = estacao.sensores
            data = [sensor.json() for sensor in sensores]
            return {"resources": data}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND

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

        try:
            sensor = Sensor(tipo=data["tipo"],
                            descricao=data["descricao"],
                            params=data["params"],
                            estacao_id=estacao_id)

            db.session.add(sensor)
            db.session.commit()

            return {"created": sensor.json()}, HTTP_RESPONSE_CREATED

        except IntegrityError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND


class ApiSensorId(Resource):
    def get(self, sensor_id):
        try:
            sensor = Sensor.query.get(sensor_id)
            return {"resource": sensor.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND

    @jwt_required()
    def put(self, sensor_id):
        parser = reqparse.RequestParser()
        parser.add_argument("tipo", type=str)
        parser.add_argument("descricao", type=str)
        parser.add_argument("params", type=str)

        data = parser.parse_args()

        try:
            sensor = Sensor.query.get(sensor_id)

            sensor.tipo = data["tipo"] if data["tipo"] else sensor.tipo
            sensor.descricao = (data["descricao"]
                                if data["descricao"] else sensor.descricao)
            sensor.params = (data["params"]
                             if data["params"] else sensor.params)

            db.session.add(sensor)
            db.session.commit()

            return {"updated": sensor.json()}

        except (AttributeError, IntegrityError):
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND

    @jwt_required()
    def delete(self, sensor_id):
        try:
            sensor = Sensor.query.get(sensor_id)
            db.session.delete(sensor)
            db.session.commit()
            return {"deleted": sensor.json()}

        except (IntegrityError, UnmappedInstanceError):
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND


class ApiSensorIdParam(Resource):
    def get(self, sensor_id, param):
        try:
            sensor = Sensor.query.get(sensor_id)
            leituras = [
                leitura.json() for leitura in sensor.leituras
                if leitura.param == param
            ]
            return {"resource": leituras}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND

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

        try:
            leitura = Leitura(datahora=datahora,
                              valor=data["valor"],
                              param=param,
                              sensor_id=sensor_id)

            db.session.add(leitura)
            db.session.commit()
            return {"created": leitura.json()}, HTTP_RESPONSE_CREATED

        except IntegrityError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND


class ApiSensorIdParamLast(Resource):
    def get(self, sensor_id, param, qty):
        try:
            sensor = Sensor.query.get(sensor_id)
            leituras = [
                leitura.json() for leitura in sensor.leituras
                if leitura.param == param
            ]
            llen = len(leituras)
            if llen > 0:
                return {"resources": leituras[-min([qty, llen]):]}
            return {"resources": []}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND
