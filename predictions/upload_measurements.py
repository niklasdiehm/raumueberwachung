import pandas as pd
import requests
from tqdm import tqdm

middleware_url = "https://fa-roomitor.azurewebsites.net/api/measurements"
middleware_api_key = "VOXG7U915GhnWo1dRCd-wuNrhgM897uDp4Lae4-kTKZCAzFu7O0DIA=="

data = pd.read_excel("Testdaten.xlsx")
print(data.head())
for index, row in tqdm(data.iterrows(), total=data.shape[0]):
    # hatte bis 3400 funktioniert
    if (index <= 3422):
        continue
    data = {
        "deviceID": "2187733e6049fabe904a1a730fe7c457",
        "measurementName": "currentPersonCount",
        "measurementValue": row["personCount"],
        "timestamp": row["timestamp_new"].strftime("%Y-%m-%d %H:%M:%S"),
        "roomName": "A457"
    }
    data1 = {
        "deviceID": "2187733e6049fabe904a1a730fe7c457",
        "measurementName": "currentTemperature",
        "measurementValue": row["temperature"],
        "timestamp": row["timestamp_new"].strftime("%Y-%m-%d %H:%M:%S"),
        "roomName": "A457"
    }
    data2 = {
        "deviceID": "2187733e6049fabe904a1a730fe7c457",
        "measurementName": "currentHumidity",
        "measurementValue": row["humidity"],
        "timestamp": row["timestamp_new"].strftime("%Y-%m-%d %H:%M:%S"),
        "roomName": "A457"
    }
    requests.post(middleware_url+"?code="+middleware_api_key, json=data)
    requests.post(middleware_url+"?code="+middleware_api_key, json=data1)
    requests.post(middleware_url+"?code="+middleware_api_key, json=data2)
