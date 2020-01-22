FROM python:3-alpine
EXPOSE 1883
RUN apk update && apk add mosquitto-clients
RUN python -m pip install --upgrade pip
RUN pip3 install paho-mqtt
RUN pip3 install ibm-cos-sdk
RUN pip3 install opencv-python

COPY cloud_forward_cos.py /
ENTRYPOINT python cloud_forward_cos.py
