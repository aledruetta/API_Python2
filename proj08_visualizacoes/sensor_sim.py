from time import sleep
from random import random, choice
from datetime import datetime

import requests

auth = {"email": "alvaro@gmail.com", "password": "12345678"}
URL = "http://localhost:5000/token"
response = requests.post(URL, json=auth)
token = response.json()['access_token']

sensor = {"id": 1, "parametros": {"temp": [10, 38], "umidade": [50, 90]}}

for param in sensor["parametros"]:
    url = f"http://localhost:5000/api/v1.1/sensor/{sensor['id']}/{param}"
    l_min = sensor["parametros"][param][0]
    l_max = sensor["parametros"][param][1]

    valor = random() * (l_max - l_min) + l_min

    while True:
        valor *= 1 + choice(range(-5, 6)) / 100

        leitura = {
            "valor": f"{valor:.2f}",
            "datahora": int(datetime.timestamp(datetime.now()))
        }

        response = requests.post(url,
                                 json=leitura,
                                 headers={"Authorization": f"jwt {token}"})
        sleep(1)

        print(response.json())
