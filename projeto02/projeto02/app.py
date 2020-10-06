from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/<int:id>")
    def api(id):
        return "Teste " + str(id)

    return app
