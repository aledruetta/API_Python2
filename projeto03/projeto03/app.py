from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


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
        "estacao_id", db.Integer, db.ForeignKey("estacao.id"), nullable=False
    )
    estacao = db.relationship(
        "Estacao", backref=db.backref("sensores", lazy=True)
    )

    def __repr__(self):
        return f"{self.tipo}"


@app.route("/")
def index():
    return render_template("index.html")


# listar estacoes
@app.route("/api")
def list():
    estacoes = Estacao.query.all()
    data = [estacao.json() for estacao in estacoes]
    return {"estacoes": data}


# pedindo dados do sensor que estao no banco de dados
@app.route("/api/<int:id>")
def read(id):
    estacao = Estacao.query.get(id)
    return {"estacao": estacao.json()}


# criar estacao no banco de dados
@app.route("/api", methods=["POST"])
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


# enviando dados para serem salvos
@app.route("/api/<int:id>", methods=["POST"])
def update(id):
    data = request.get_json()
    estacao = Estacao.query.get(id)

    estacao.local = data.get("local", estacao.local)
    estacao.latitude = data.get("latitude", estacao.latitude)
    estacao.longitude = data.get("longitude", estacao.longitude)

    db.session.add(estacao)
    db.session.commit()

    return {"msg": estacao.json()}


# deletar dados no banco de dados
@app.route("/api/<int:id>/del", methods=["POST"])
def delete(id):
    estacao = Estacao.query.get(id)

    db.session.delete(estacao)
    db.session.commit()

    return {"msg": "Success!"}
