from datetime import datetime

import requests

auth = {"email": "alvaro@gmail.com", "password": "12345678"}
url = "http://localhost:5000/token"
response = requests.post(url, json=auth)
token = response.json()['access_token']

sensor_id = 1
param = "temp"
url = f"http://localhost:5000/api/v1.1/sensor/{sensor_id}/{param}"
valor = 23.5
leitura = {"valor": valor, "datahora": int(datetime.timestamp(datetime.now()))}
response = requests.post(url,
                         json=leitura,
                         headers={"Authorization": f"jwt {token}"})
print(response)
