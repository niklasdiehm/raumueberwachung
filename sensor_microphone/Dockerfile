FROM balenalib/rpi-raspbian

# Install dependencies
RUN apt-get update && \
    apt-get install -yq \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    i2c-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Enable the v4l2 driver for the Raspberry Pi camera
#RUN printf "bcm2835-v4l2\n" >> /etc/modules

RUN pip3 install --upgrade pip 

RUN pip3 install adafruit-circuitpython-ads1x15 RPi.GPIO

WORKDIR /usr/src/app

COPY ./microphone_sensor.py /usr/src/app/microphone_sensor.py

CMD ["python3", "/usr/src/app/microphone_sensor.py"]