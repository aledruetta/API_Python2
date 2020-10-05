#!/usr/bin/env python3

from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/")
def index():
    name = request.args.get("name", None)
    return render_template("index.html", name=name)


@app.route("/api/<int:id>")
def sensor(id):
    return "Este é o sensor " + str(id)
