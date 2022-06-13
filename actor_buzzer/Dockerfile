FROM balenalib/raspberrypi3-debian:stretch-20190612

# Install dependencies
RUN apt-get update && \
    apt-get install -yq \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Enable the v4l2 driver for the Raspberry Pi camera
#RUN printf "bcm2835-v4l2\n" >> /etc/modules

RUN pip3 install --upgrade pip 

RUN pip3 install pip install RPi.GPIO requests

WORKDIR /usr/src/app

COPY ./buzzer.py /usr/src/app/buzzer.py

CMD ["python3", "/usr/src/app/buzzer.py"]