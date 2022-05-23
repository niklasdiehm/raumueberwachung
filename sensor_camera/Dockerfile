FROM balenalib/raspberrypi3-debian

# Install dependencies
RUN apt-get update && \
    apt-get install -yq \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    python3-opencv \
    i2c-tools \
    libatlas-base-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libatlas-base-dev \
    libjasper-dev \
    libwebp-dev\
    libtiff5 \
    libopenjp2-7 \
    libpng16-16 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Enable the v4l2 driver for the Raspberry Pi camera
# RUN printf "bcm2835-v4l2\n" >> /etc/modules

WORKDIR /usr/src/app

RUN pip3 install --upgrade pip

RUN pip3 install opencv-contrib-python-headless==4.5.3.56

RUN pip3 install --upgrade numpy

COPY ./camera.py /usr/src/app/camera.py
COPY ./models /usr/src/app/models/

CMD ["python3", "/usr/src/app/camera.py"]