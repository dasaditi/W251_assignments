FROM python:3-alpine

EXPOSE 1883

RUN apk update && apk add mosquitto-clients
RUN python -m pip install --upgrade pip

RUN pip3 install paho-mqtt

COPY edge_forward_message.py /

ENTRYPOINT python edge_forward_message.py