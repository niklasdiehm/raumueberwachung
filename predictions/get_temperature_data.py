import requests
from datetime import datetime, timedelta
from datetime import timezone
import pandas as pd

# Get the data from the Azure IoT Hub
# We want to get the data from the last 7 days
# we iterate over the hours and get the data for each hour
# after that, we append the data to a list and output a csv file

current_date = datetime.strptime("2022-07-07 0:00:00", "%Y-%m-%d %H:%M:%S")
date_seven_days_before = current_date - timedelta(days=7)

results = []
while (date_seven_days_before < current_date):
    date_seven_days_before = date_seven_days_before + timedelta(hours=1)
    request = requests.get("https://fa-roomitor.azurewebsites.net/api/predictions?code=VOXG7U915GhnWo1dRCd-wuNrhgM897uDp4Lae4-kTKZCAzFu7O0DIA==" +
                           "&timestamp[after]=" +
                           date_seven_days_before.strftime("%Y-%m-%d %H:%M:%S") +
                           "&timestamp[before]=" +
                            (date_seven_days_before + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S") +
                           "&deviceID=2187733e6049fabe904a1a730fe7c457" + 
                           "&measurementName=temperature")
    print(request)
    results.extend(request.json())
df = pd.DataFrame.from_records(results)
df.drop(columns=["_self", "_etag", "_attachments", "_ts", "id", "_rid"], inplace=True)
print(df.head())
df.to_excel("humidity_data.xlsx")
