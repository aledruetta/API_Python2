from time import sleep
from random import random, choice
from datetime import datetime
from projeto.ext.api.models import Estacao, Sensor, Leitura
from projeto.ext.db import db

import requests
import numpy as np

MIN_VAR = -0.5
MAX_VAR = 0.5
LINSPACE = np.linspace(MIN_VAR, MAX_VAR, 10)

MIN_TEMP = 10
MAX_TEMP = 40
MIN_UMID = 50
MAX_UMID = 100


def create_all():
    estacoes = [
        Estacao(local="Ubatuba", latitude="-23.43389", longitude="-45.07111"),
        Estacao(local="Caraguatatuba",
                latitude="-23.62028",
                longitude="-45.41306"),
        Estacao(local="Cunha", latitude="-23.07444", longitude="-44.95972")
    ]

    sensores = [
        Sensor(tipo="DHT11",
               descricao="Sensor temperatura e umidade",
               params="temperatura,umidade",
               estacao_id=1),
        Sensor(tipo="DHT22",
               descricao="Sensor temperatura e umidade",
               params="temperatura,umidade",
               estacao_id=2),
        Sensor(tipo="BMP180",
               descricao="Sensor temperatura e umidade",
               params="temperatura",
               estacao_id=3)
    ]

    for estacao in estacoes:
        db.session.add(estacao)
        db.session.commit()

    for sensor in sensores:
        db.session.add(sensor)
        db.session.commit()


def post(url, leitura, token):
    response = requests.post(url,
                             json={
                                 "valor": f"{leitura.valor:.2f}",
                                 "datahora": getDatahora()
                             },
                             headers={"Authorization": f"jwt {token}"})
    print(response.json())


def getDatahora():
    return int(datetime.timestamp(datetime.now()))


def simular():
    auth = {"email": "admin@gmail.com", "password": "12345678"}
    URL = "http://localhost:5000/token"
    token = requests.post(URL, json=auth).json()['access_token']

    sensores = Sensor.query.all()

    # Cria valores iniciais
    for sensor in sensores:
        for param in sensor.params.split(","):
            if param == "temperatura":
                pmin = MIN_TEMP
                pmax = MAX_TEMP
            elif param == "umidade":
                pmin = MIN_UMID
                pmax = MAX_UMID

            url = f"http://localhost:5000/api/v1.1/sensor/{sensor.id}/{param}"
            valor = random() * (pmax - pmin) + pmin
            leitura = Leitura(valor=valor, datahora=getDatahora())
            post(url, leitura, token)

    # Simula geração de leituras a cada 1 segundo
    while True:
        sleep(1)

        for sensor in sensores:
            for param in sensor.params.split(","):
                url = f"http://localhost:5000/api/v1.1/sensor/{sensor.id}/{param}"
                i = 1
                while (i < len(sensor.leituras)
                       and sensor.leituras[-i].param != param):
                    i += 1
                last = float(sensor.leituras[-i].valor)
                valor = last + random() * choice(LINSPACE)
                leitura = Leitura(valor=valor, datahora=getDatahora())
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
