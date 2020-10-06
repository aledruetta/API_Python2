from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    # pedindo dados do sensor que estao no banco de dados
    @app.route("/api/<int:id>")
    def read(id):
        pass

    # enviando dados para serem salvos
    @app.route("/api/<int:id>", method=["POST"])
    def update(id):
        pass

    # deletar dados no banco de dados
    @app.route("/api/<int:id>")
    def delete(id):
        pass

    return app
