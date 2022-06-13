import RPi.GPIO as GPIO
import time
import os
import requests
from datetime import datetime, timedelta
from datetime import timezone

actors_on = os.environ.get("ACTORS_ON")
if actors_on != "1":
    exit()

GPIO.setmode(GPIO.BCM)
# Hier wird der Ausgangs-Pin deklariert, an dem der Buzzer angeschlossen ist.
Buzzer_PIN = 24
GPIO.setup(Buzzer_PIN, GPIO.OUT, initial=GPIO.LOW)

middleware_url = os.environ.get("MIDDLEWARE_URL")
middleware_api_key = os.environ.get("MIDDLEWARE_API_KEY")
device_id = os.environ.get("RESIN_DEVICE_UUID")
room_name = os.environ.get("ROOM_NAME")
measurement_interval_secs = int(os.environ.get("MEASUREMENT_INTERVAL_SECS"))
actors_humidity_threshold_percent = int(
    os.environ.get("ACTORS_HUMIDITY_THRESHOLD_PERCENT")
)

# Hauptprogrammschleife
try:
    while True:
        time_to_middleware = datetime.now(timezone.utc) - timedelta(
            seconds=measurement_interval_secs * 3
        )
        request = requests.get(middleware_url +
                               "?code=" + middleware_api_key +
                               "&deviceID=" + device_id +
                               "&timestamp[after]=" +
                               time_to_middleware.strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ) +
                               "&measurementName=currentHumidity")
        data = request.json()
        # Hier wird die aktuelle Luftfeuchtigkeit ermittelt
        newlist = sorted(data, key=lambda d: d['timestamp'])
        if len(newlist) > 0:
            current_humidity = newlist[-1]['measurementValue']
        else:
            current_humidity = 0
        print("Current humidity: " + str(current_humidity))
        print("Humidity threshold: " + str(actors_humidity_threshold_percent))
        # Wenn die Luftfeuchtigkeit oberhalb des Schwellwertes ist,
        # wird der Buzzer für eine Sekunde eingeschaltet und dann wieder ein
        # Intervall abgewartet. Ansonsten wird das Intervall abgewartet.
        if current_humidity > actors_humidity_threshold_percent:
            GPIO.output(Buzzer_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(Buzzer_PIN, GPIO.LOW)
        time.sleep(measurement_interval_secs)

# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
