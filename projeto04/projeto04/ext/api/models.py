from projeto04.ext.db import db


class Estacao(db.Model):
    __tablename__ = "estacao"

    id = db.Column("id", db.Integer, primary_key=True)
    local = db.Column("local", db.String(255), nullable=False)
    latitude = db.Column("latitude", db.String(255), nullable=False)
    longitude = db.Column("longitude", db.String(255), nullable=False)

    def json(self):
        return {
            "local": self.local,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    def __repr__(self):
        return f"{self.local} [{self.latitude}, {self.longitude}]"


class Sensor(db.Model):
    __tablename__ = "sensor"

    id = db.Column("id", db.Integer, primary_key=True)
    tipo = db.Column("tipo", db.String(255), nullable=False)

    estacao_id = db.Column(
        "estacao_id",
        db.Integer, db.ForeignKey("estacao.id"), nullable=False
    )
    estacao = db.relationship(
        "Estacao", backref=db.backref("sensores", lazy=True)
    )

    def __repr__(self):
        return f"{self.tipo}"
