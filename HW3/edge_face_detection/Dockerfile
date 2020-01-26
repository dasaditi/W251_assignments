FROM ubuntu

RUN apt-get update
RUN apt-get install -y software-properties-common

RUN apt-get update && apt-get install -y \
    build-essential\
    curl \
    git \
    python3.6 \
    python3-pip \
    vim \
    cmake \
    libhdf5-dev \
    python3-numpy \
    python3-setuptools \
    libgtk2.0-dev \
    python3-wheel\
    python3-dev\
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libdc1394-22-dev \
    unzip\
    pkg-config \
    libgtk-3-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    gfortran \
    libatlas-base-dev


RUN cd \
    && git clone https://github.com/opencv/opencv.git \
    && git clone https://github.com/opencv/opencv_contrib.git \
    && cd opencv \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make -j8 \
    && make install \
    && cd 
    
RUN apt-get install -y mosquitto-clients
RUN pip3 install paho-mqtt

EXPOSE 1883
COPY haarcascade_frontalface_default.xml /
COPY edge_face_detection.py /
COPY test_face_detection.py /
#ENTRYPOINT python3 edge_face_detection.py
