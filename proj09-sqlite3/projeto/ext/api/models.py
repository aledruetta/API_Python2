from datetime import datetime

from projeto.ext.db import db


class Estacao(db.Model):
    __tablename__ = "estacao"

    id = db.Column("id", db.Integer, primary_key=True)
    local = db.Column("local", db.String(255), nullable=False)
    latitude = db.Column("latitude", db.String(255), nullable=False)
    longitude = db.Column("longitude", db.String(255), nullable=False)

    def get_sensor(self, sensor_id):
        for sensor in self.sensores:
            if sensor.id == sensor_id:
                return sensor

    def json(self):
        return {
            "id": self.id,
            "local": self.local,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    def __repr__(self):
        return f"{self.local} [{self.latitude}, {self.longitude}]"


class Sensor(db.Model):
    __tablename__ = "sensor"

    id = db.Column("id", db.Integer, primary_key=True)
    tipo = db.Column("tipo", db.String(255), nullable=False)
    descricao = db.Column("descricao", db.String(255), nullable=False)
    params = db.Column("params", db.String(255), nullable=False)

    estacao_id = db.Column("estacao_id",
                           db.Integer,
                           db.ForeignKey("estacao.id"),
                           nullable=False)
    estacao = db.relationship("Estacao",
                              backref=db.backref("sensores",
                                                 cascade="all, delete-orphan",
                                                 lazy=True))

    def json(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "params": self.params,
            "estacao_id": self.estacao_id,
        }

    def __repr__(self):
        return f"{self.tipo}"


class Leitura(db.Model):
    __tablename__ = "leitura"

    id = db.Column("id", db.Integer, primary_key=True)
    param = db.Column("param", db.String(255), nullable=False)
    valor = db.Column("valor", db.String(255), nullable=False)
    datahora = db.Column("datahora", db.DateTime(), nullable=False)

    sensor_id = db.Column("sensor_id",
                          db.Integer,
                          db.ForeignKey("sensor.id"),
                          nullable=False)
    sensor = db.relationship("Sensor",
                             backref=db.backref("leituras",
                                                cascade="all, delete-orphan",
                                                lazy=True))

    def datahora_str(self):
        return self.datahora.strftime("%d-%b-%Y (%H:%M:%S.%f)")

    def json(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "datahora": datetime.timestamp(self.datahora),
            "param": self.param,
            "valor": self.valor,
        }

    def __repr__(self):
        return f"{self.datahora_str()} - {self.param}: {self.valor}"
