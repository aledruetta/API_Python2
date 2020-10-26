from time import sleep
from random import random, choice
from datetime import datetime

import requests
import numpy as np

auth = {"email": "alvaro@gmail.com", "password": "12345678"}
URL = "http://localhost:5000/token"
response = requests.post(URL, json=auth)
token = response.json()['access_token']

sensor = {"id": 1, "parametros": {"temp": [10, 38], "umidade": [50, 90]}}

for param in sensor["parametros"].keys():
    pmin = min(sensor["parametros"][param])
    pmax = max(sensor["parametros"][param])
    sensor["parametros"][param].append(random() * (pmax - pmin) + pmin)

while True:
    for param in sensor["parametros"]:
        url = f"http://localhost:5000/api/v1.1/sensor/{sensor['id']}/{param}"

        sensor["parametros"][param][2] += random() * choice(
            np.linspace(-0.2, 0.2, 10))

        leitura = {
            "valor": f"{sensor['parametros'][param][2]:.2f}",
            "datahora": int(datetime.timestamp(datetime.now()))
        }

        response = requests.post(url,
                                 json=leitura,
                                 headers={"Authorization": f"jwt {token}"})
        sleep(1)

        print(response.json())
