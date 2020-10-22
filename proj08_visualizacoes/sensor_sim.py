from time import sleep
from random import random, randint
from datetime import datetime

import requests

auth = {"email": "alvaro@gmail.com", "password": "12345678"}
URL = "http://localhost:5000/token"
response = requests.post(URL, json=auth)
token = response.json()['access_token']

SENSOR_ID = 1
PARAM = "temp"
url = f"http://localhost:5000/api/v1.1/sensor/{SENSOR_ID}/{PARAM}"

TEMP_MIN = 26
TEMP_MAX = 38
VARIACAO = 0.1
valor = random() * (TEMP_MAX - TEMP_MIN) + TEMP_MIN
valores = [-VARIACAO*2, -VARIACAO, 0, VARIACAO, VARIACAO*2]

for i in range(500):
    num = randint(0, 4)
    valor += valores[num]

    leitura = {
        "valor": valor,
        "datahora": int(datetime.timestamp(datetime.now()))
    }

    response = requests.post(url,
                             json=leitura,
                             headers={"Authorization": f"jwt {token}"})
    sleep(1)

    print(response.json())
