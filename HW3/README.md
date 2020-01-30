# HW3 assignment


The overall goal of the assignment is to be able to capture faces in a video stream coming from the edge in real time, transmit them to the cloud in real time, and for now, just save these faces in the cloud for long term storage(S3-object storage).

## Things that needs to be done on TX2
- a) Read video from a USB webcam. Use OpenCV and write an application that scans the video frames coming from the connected USB camera for face detection.When one or more faces are detected in the frame, the application should cut them out of the frame and send to cloud storage via MQTT.

- b) We will be using an MQTT client to send and receive messages, and MQTT broker as the server component of this architecture.Install a local MQTT broker in the TX2 and your face detector sends its messages to this broker first.

- c) We write another component that receives these messages from the local broker, and sends them to the cloud [MQTT broker].	
- d) So in total there are three deocker container ruuning in TX2
```	
	i) edge_face_detection
		sudo docker build -t edge_face_detection .
		Give Access: xhost local:root
		sudo docker run --privileged --name edge_face_detection  --network hw03  -v /dev/video1:/dev/video1 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -ti edge_face_detection
	ii) edge_mqtt_broker
		sudo docker build -t edge_mosquitto .
		sudo docker run --name edge_mosquitto --network hw03  -ti edge_mosquitto
	ii) edge_mqtt_forwarder
		sudo docker build -t edge_mqtt_forwarder .	
		sudo docker run --name edge_mqtt_forwarder --network hw03  -ti edge_mqtt_forwarder
```	

### All these three containers are connected via docker network 	

```
	docker network create --driver bridge hw03
```

- e) In order for the docker to get access to the camera hardware we need to provide priveledges to the container. We need to run xhost local:root before running the docker container.

## Things that needs to be done on Cloud

- a) you need to provision a lightweight virtual machine (1-2 CPUs and 2-4 G of RAM should suffice) 

- b) Run an MQTT broker. The broker is responsible for receiving all messages from TX2.The MQTT protocol is based on TCP/IP. Both the client and the broker need to have a TCP/IP stack.

- c) Once the message is received in cloud , it will be converted back to image and saved in S3 storage.

- d) So in total there are two deocker container ruuning in cloud . And in cloud too we will be linking the containers through docker network.

```
	i) Create an alpine linux - based mosquitto Broker
		docker build -t cloud_mosquitto .
		docker run --name cloud_mosquitto --network hw03  -p 1883:1883 -ti cloud_mosquitto

	ii) Create a message forwarder container to S3:
		docker build -t cloud_forwarder .
		docker run --name subscriber --network hw03  -ti cloud_forwarder 
```
## Here is a link to the image stored in S3
https://w251-aditi-bucket.s3.us.cloud-object-storage.appdomain.cloud/face_01_26_2020T03_15_12.png
