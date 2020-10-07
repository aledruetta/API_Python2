from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Estacao(db.Model):
    __tablename__ = "estacao"

    id = db.Column(db.Integer, primary_key=True)
    local = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"{self.local} [{self.latitude}, {self.longitude}]"


class Sensor(db.Model):
    __tablename__ = "sensor"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(255), nullable=False)

    estacao_id = db.Column(
        db.Integer, db.ForeignKey('estacao.id'), nullable=False)
    estacao = db.relationship(
        'Estacao', backref=db.backref('sensores', lazy=True))

    def __repr__(self):
        return f"{self.tipo}"


@app.route("/")
def index():
    return render_template("index.html")


# listar estacoes
@app.route("/api")
def list():
    with sqlite3.connect("test.db") as conn:
        cur = conn.cursor()
        qry = """
            SELECT * FROM estacao
        """
        cur.execute(qry)
        data = cur.fetchall()
        conn.commit()

    return {"estacoes": data}


# pedindo dados do sensor que estao no banco de dados
@app.route("/api/<int:id>")
def read(id):
    with sqlite3.connect("test.db") as conn:
        cur = conn.cursor()
        qry = """
            SELECT * FROM estacao
            WHERE id = ?
        """
        cur.execute(qry, (str(id),))
        data = cur.fetchone()
        conn.commit()

    return {"estacao": data}


# criar estacao no banco de dados
@app.route("/api", methods=["POST"])
def create():
    data = request.get_json()

    estacao = Estacao(data['local'], data['latitude'], data['longitude'])
    db.session.add(estacao)
    db.session.commit()

    return {"msg": "Success!"}


# enviando dados para serem salvos
@app.route("/api/<int:id>", methods=["POST"])
def update(id):
    data = request.get_json()

    with sqlite3.connect("test.db") as conn:
        cur = conn.cursor()
        qry = """
                UPDATE estacao SET local = ?, latitude = ?, longitude = ?
                WHERE id = ?
        """
        cur.execute(
            qry,
            (data['local'], data['latitude'], data['longitude'], str(id)),
        )
        conn.commit()

    return {"msg": "Success!"}


# deletar dados no banco de dados
@app.route("/api/<int:id>/del", methods=["POST"])
def delete(id):
    with sqlite3.connect("test.db") as conn:
        cur = conn.cursor()
        qry = """
                DELETE FROM estacao
                WHERE id = ?
        """
        cur.execute(qry, str(id))
        conn.commit()

    return {"msg": "Success!"}
