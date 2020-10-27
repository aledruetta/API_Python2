from time import sleep
from random import random, choice
from datetime import datetime

import requests
import numpy as np

auth = {"email": "alvaro@gmail.com", "password": "12345678"}
URL = "http://localhost:5000/token"
response = requests.post(URL, json=auth)
TOKEN = response.json()['access_token']

MIN_VAR = -0.5
MAX_VAR = 0.5
LINSPACE = np.linspace(MIN_VAR, MAX_VAR, 10)

sensor = {"id": 1, "parametros": {"temp": [10, 38], "umidade": [50, 90]}}

for param in sensor["parametros"].keys():
    pmin = min(sensor["parametros"][param])
    pmax = max(sensor["parametros"][param])
    sensor["parametros"][param].append(random() * (pmax - pmin) + pmin)

while True:

    for param in sensor["parametros"]:
        url = f"http://localhost:5000/api/v1.1/sensor/{sensor['id']}/{param}"

        sensor["parametros"][param][2] += random() * choice(LINSPACE)

        leitura = {
            "valor": f"{sensor['parametros'][param][2]:.2f}",
            "datahora": int(datetime.timestamp(datetime.now()))
        }

        response = requests.post(url,
                                 json=leitura,
                                 headers={"Authorization": f"jwt {TOKEN}"})
        sleep(1)

        print(response.json())
