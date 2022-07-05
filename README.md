# Codestruktur

In den Unterordnern "actor_buzzer", "actor_led", "sensor_camera", "sensor_microphone" und "sensor_temperature" befinden sich die Dateien
für die einzelnen Aktoren und Sensoren. Pro Service ist ein Dockerfile vorhanden, welches einen Dockercontainer auf dem Gerät startet. Damit die balenaCloud die einzelnen
Container starten kann, wird in der Datei "docker-compose.yml" jeder Service eingetragen. In der Datei "balena.yml" sind einige Konfigurationen, welche
für die balenaCloud essentiell sind, definiert.

# Gerät in der balenaCloud registrieren

Um ein Gerät in der balenaCloud zu registrieren, muss innerhalb der existierenden Fleet "Raumueberwachung" unter "Devices" auf "Add device" geklickt werden.
Dann können die gerätespezifischen Einstellungen vorgenommen werden und das Image heruntergeladen werden. Nach dem Installieren des Images auf der Speicherkarte
kann das Gerät gestartet werden. Es verbindet sich automatisch mit der balenaCloud und lädt die Services herunter.

# Code für die Services auf die balenaCloud hochladen

Um den Code für die Services auf die balenaCloud hochzuladen, müssen die folgenden Befehle auf der Kommandozeile ausgeführt werden:

```bash
balena login
balena push iot_gm_raumueberwachung/raumueberwachung
```

# Vorhersage der Temperaturwerte

Der Code für die Vorhersage der Sensorwerte befindet sich im Unterordner "predictions".
Zuerst werden mittels der Datei "get_past_data.py" die Vergangenheitsdaten heruntergeladen.
Danach wird mittels der Datei "predict_values.py" die Vorhersage durchgeführt und die Vorhersagen an die Middleware gesendet.
In jeder Datei kann angepasst werden, welche Daten heruntergeladen werden sollen (Luftfeuchtigkeit, Temperatur, Auslastung).
