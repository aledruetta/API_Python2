from flask import Flask, render_template, request
import sqlite3


def create_app():
    app = Flask(__name__)

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
        pass

    # criar estacao no banco de dados
    @app.route("/api", methods=["POST"])
    def create():
        data = request.get_json()

        with sqlite3.connect("test.db") as conn:
            cur = conn.cursor()
            qry = """
                    INSERT INTO estacao (local, latitude, longitude)
                    VALUES (?, ?, ?)
            """
            cur.execute(
                qry, (data['local'], data['latitude'], data['longitude']))
            conn.commit()

        return {"msg": "Success!"}

    # enviando dados para serem salvos
    @app.route("/api/<int:id>", methods=["POST"])
    def update(id):
        pass

    # deletar dados no banco de dados
    @app.route("/api/<int:id>", methods=["DELETE"])
    def delete(id):
        pass

    return app
