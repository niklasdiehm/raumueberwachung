import time
import board
import adafruit_dht
import requests
import os
from datetime import datetime
from datetime import timezone

# Initialize device
dhtDevice = adafruit_dht.DHT11(board.D23, use_pulseio=False)

# Retrieve environment variables
middleware_url = os.environ.get("MIDDLEWARE_URL")
middleware_api_key = os.environ.get("MIDDLEWARE_API_KEY")
device_id = os.environ.get("RESIN_DEVICE_UUID")
room_name = os.environ.get("ROOM_NAME")
measurement_interval_secs = int(os.environ.get("MEASUREMENT_INTERVAL_SECS"))

while True:
    try:
        # Reading temerpature and humidity
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity / 100
        data = {
            "deviceID": device_id,
            "measurementName": "currentTemperature",
            "measurementValue": temperature_c,
            "timestamp": datetime.now(timezone.utc)
            .strftime("%Y-%m-%d %H:%M:%S"),
            "roomName": room_name
        }
        # Send temperature and humidity to middleware
        requests.post(middleware_url+"?code="+middleware_api_key, json=data)
        data["measurementName"] = "currentHumidity"
        data["measurementValue"] = humidity * 100
        requests.post(middleware_url+"?code="+middleware_api_key, json=data)
        # Print temperature and humidity on command line
        print("Temp: {temperature_c}".format(temperature_c=temperature_c))
        print("Humidity: {humidity}% ".format(humidity=humidity*100))

    except RuntimeError as error:
        # if an error occurs while reading the temperature, try again
        # after one second
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        print(error.args[0])
        dhtDevice.exit()
        raise error
    # if sucessful, wait for measurement interval seconds before next measurement
    time.sleep(measurement_interval_secs)
