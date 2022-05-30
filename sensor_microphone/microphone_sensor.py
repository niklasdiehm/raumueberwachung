import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import requests
import os
from datetime import datetime
from datetime import timezone

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Retrieve environment variables
middleware_url = os.environ.get("MIDDLEWARE_URL")
middleware_api_key = os.environ.get("MIDDLEWARE_API_KEY")
device_id = os.environ.get("RESIN_DEVICE_UUID")

while True:
    values = []
    voltages = []
    for _ in range(120):
        values.append(chan.value)
        voltages.append(chan.voltage)
        time.sleep(0.5)
    average_value = sum(values) / len(values)
    # Kalibrated decibel linear regression function
    average_decibel = -38804.00 + 21 * average_value
    print("{:>5} value".format(average_value))
    print("{:>5} decibel".format(average_decibel))
    data = {
        "deviceID": device_id,
        "measurement": "currentVolume",
        "value": average_decibel,
        "timestamp": datetime.now(timezone.utc)
        .strftime("%Y-%m-%d %H:%M:%S")
    }
    requests.post(middleware_url+"?code="+middleware_api_key, json=data)
