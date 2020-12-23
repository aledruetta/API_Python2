from datetime import datetime
from random import choice, random
from time import sleep

import numpy as np
import requests
from projeto.ext.api.models import Estacao, Leitura, Sensor, SensorTipo
from projeto.ext.db import db

MIN_VAR = -1
MAX_VAR = 1
LINSPACE = np.linspace(MIN_VAR, MAX_VAR, 10)

MIN_TEMP = 10
MAX_TEMP = 40
MIN_UMID = 50
MAX_UMID = 100
MIN_LUMI = 30
MAX_LUMI = 1024
MIN_CHUV = 5
MAX_CHUV = 100
MIN_SOM = 30
MAX_SOM = 100
MIN_PRES = 30
MAX_PRES = 100

VERSAO = "v1.2"


def create_all():
    estacoes = {
        "ubatuba":
        Estacao(local="Ubatuba", latitude="-23.43389", longitude="-45.07111"),
        "caragua":
        Estacao(local="Caraguatatuba",
                latitude="-23.62028",
                longitude="-45.41306"),
        "cunha":
        Estacao(local="Cunha", latitude="-23.07444", longitude="-44.95972")
    }

    tipos = {
        "dht11":
        SensorTipo(codigo="DHT11",
                   descricao="Sensor temperatura e umidade",
                   params="temp_ambiente,umid_relativa"),
        "ldr":
        SensorTipo(codigo="LDR",
                   descricao="Sensor de luminosidade",
                   params="luminosidade"),
        "ds18b20":
        SensorTipo(codigo="DS18B20",
                   descricao="Sensor de temperatura digital",
                   params="temp_agua"),
        "solo":
        SensorTipo(codigo="LM393_solo",
                   descricao="Sensor de umidade do solo",
                   params="umid_solo"),
        "chuva":
        SensorTipo(codigo="LM393_chuva",
                   descricao="Sensor de chuva",
                   params="chuva"),
        "som":
        SensorTipo(codigo="LM393_som", descricao="Sensor de som",
                   params="som"),
        "bmp180":
        SensorTipo(codigo="BMP180",
                   descricao="Sensor de altitude e pressão",
                   params="altitude,pressao"),
        "dht22":
        SensorTipo(codigo="DHT22",
                   descricao="Sensor temperatura e umidade",
                   params="temp_ambiente,umid_relativa")
    }

    sensores = [
        Sensor(tipo=tipos["dht11"], estacao=estacoes["ubatuba"]),
        Sensor(tipo=tipos["ldr"], estacao=estacoes["ubatuba"]),
        Sensor(tipo=tipos["ds18b20"], estacao=estacoes["ubatuba"]),
        Sensor(tipo=tipos["solo"], estacao=estacoes["ubatuba"]),
        Sensor(tipo=tipos["chuva"], estacao=estacoes["ubatuba"]),
        Sensor(tipo=tipos["som"], estacao=estacoes["ubatuba"]),
        Sensor(tipo=tipos["bmp180"], estacao=estacoes["ubatuba"]),
        Sensor(tipo=tipos["dht22"], estacao=estacoes["caragua"]),
        Sensor(tipo=tipos["bmp180"], estacao=estacoes["cunha"]),
    ]

    for estacao in estacoes.values():
        db.session.add(estacao)
        db.session.commit()

    for sensor in sensores:
        db.session.add(sensor)
        db.session.commit()

def get_datahora():
    return int(datetime.timestamp(datetime.now()))

def post(url, leitura, token):
    response = requests.post(url,
                             json={
                                 "valor": f"{leitura.valor:.2f}",
                                 "datahora": get_datahora()
                             },
                             headers={"Authorization": f"jwt {token}"})
    print(response.json())

def simular():
    auth = {"email": "admin@gmail.com", "password": "12345678"}
    url = "http://localhost:5000/token"
    token = requests.post(url, json=auth).json()['access_token']

    sensores = Sensor.query.all()
    valores_iniciais = []
    pmax = 0
    pmin = 0

    # Determina os valores iniciais para cada parámetro
    for sensor in sensores:
        valores_sensor = {}
        for param in sensor.tipo.params.split(","):
            if param.startswith("temp"):
                pmin = MIN_TEMP
                pmax = MAX_TEMP
            elif param.startswith("umid"):
                pmin = MIN_UMID
                pmax = MAX_UMID
            elif param.startswith("lumin"):
                pmin = MIN_LUMI
                pmax = MAX_LUMI
            elif param == "chuva":
                pmin = MIN_CHUV
                pmax = MAX_CHUV
            elif param == "som":
                pmin = MIN_SOM
                pmax = MAX_SOM
            elif param.startswith("pres"):
                pmin = MIN_PRES
                pmax = MAX_PRES

            valor = random() * (pmax - pmin) + pmin
            valores_sensor[param] = valor

        valores_iniciais.append(valores_sensor)
    zip_sensores = list(zip(sensores, valores_iniciais))

    # Simula geração de leituras a cada 1 segundo
    while True:
        sleep(1)

        for sensor, valores in zip_sensores:
            params = sensor.tipo.params.split(",")
            for param in params:
                url = f"http://localhost:5000/api/{VERSAO}/sensor/{sensor.id}/{param}"
                inicial = float(valores[param])
                valor = inicial + random() * choice(LINSPACE)
                leitura = Leitura(valor=valor, datahora=get_datahora())
                post(url, leitura, token)

if __name__ == "__main__":
    print("""
    Esse script não deve ser executado.
    Uso:
        - crie uma sessão interativa com `flask shell`
        - importe o módulo com `import sensor_sim`
        - chame a função com:
            `sensor_sim.create_all()`
            `sensor_sim.simular()`
""")
