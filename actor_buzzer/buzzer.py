import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Hier wird der Eingangs-Pin deklariert, an dem der Sensor angeschlossen ist.
Buzzer_PIN = 24
GPIO.setup(Buzzer_PIN, GPIO.OUT, initial=GPIO.LOW)

print("Buzzer-Test [druecken Sie STRG+C, um den Test zu beenden]")

# Hauptprogrammschleife
try:
    while True:
        print("Buzzer 1 Sekunden an")
        GPIO.output(Buzzer_PIN, GPIO.HIGH)  # Buzzer wird eingeschaltet
        time.sleep(1)  # Wartemodus für 1 Sekunde
        print("Buzzer 15 Sekunden aus")
        GPIO.output(Buzzer_PIN, GPIO.LOW)  # Buzzer wird ausgeschaltet
        time.sleep(15)

# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
    GPIO.cleanup()
