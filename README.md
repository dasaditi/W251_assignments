# W251_assignments
HW3
----
The overall goal of the assignment is to be able to capture faces in a video stream coming from the edge in real time, transmit them to the cloud in real time, 
and - for now, just save these faces in the cloud for long term storage(S3-object storage).

1) Things that needs to be done on TX2
	a) Alpine Linux as the base OS for your containers
	Reading video from a USB webcam
	b) Have a Face detector component OpenCV
		Use OpenCV and write an application that scans the video frames coming from the connected USB camera for faces.
		When one or more faces are detected in the frame, the application should cut them out of the frame and send via a binary message each.

	c) You will be using an MQTT client to send and receive messages, and MQTT broker as the server component of this architecture.
		install a local MQTT broker in the TX2 and your face detector sends its messages to this broker first.
	d) you write another component that receives these messages from the local broker, and sends them to the cloud [MQTT broker].	
	
	Details in
		i) cd edge_mqtt_broker
			docker build -t edge_mosquitto .	
			
		ii) cd edge_face_detection folder
			Build docker : docker build -t edge_face_detection .
			
		ii) Linking containers :docker network create --driver bridge hw03
		
2) Things that needs to be done on Cloud
	a) you need to provision a lightweight virtual machine (1-2 CPUs and 2-4 G of RAM should suffice) 
		Details in 
			i) "Create a virtual server from scratch through CLI"
			ii) Install Docker on Ubuntu 16 
			iii) Install Github on Ubuntu
			iv) Install Curl on Ubuntu
		
	b) Run an MQTT broker. http://mqtt.org/ 
	The broker is responsible for receiving all messages, filtering the messages, determining who is subscribed to each message, and sending the message to these subscribed clients.
	The MQTT protocol is based on TCP/IP. Both the client and the broker need to have a TCP/IP stack.
	The MQTT connection is always between one client and the broker. Clients never connect to each other directly. 
	To initiate a connection, the client sends a CONNECT message to the broker. The broker responds with a CONNACK message and a status code.
	Once the connection is established, the broker keeps it open until the client sends a disconnect command or the connection breaks.
	Implementation of MQTT is Mosquito  : Note that mqtt uses port 1883 for un-encrypted messages.

		Details in
			i) Linking containers :docker network create --driver bridge hw03
			ii) Create an alpine linux - based mosquitto Broker
					FROM alpine
					EXPOSE 1883
					RUN apk update && apk add mosquitto
					ENTRYPOINT /usr/sbin/mosquitto	
					
				docker build -t cloud_mosquitto .	
			iii) # Create an alpine linux - based message forwarder container:
					FROM python:3-alpine
					EXPOSE 1883
					RUN apk update && apk add mosquitto-clients
					RUN pip3 install paho-mqtt
					COPY forward_message.py /
					ENTRYPOINT python forward_message.py
					
				docker build -t cloud_forwarder .
			iv) Run Docker containers
				docker run --name subscriber --network hw03  -ti cloud_forwarder 
				docker run --name cloud_mosquitto --network hw03  -ti cloud_mosquitto
			
			v) Test with a sample publisher
				docker run --name publisher --network hw03 -ti alpine sh
				apk update && apk add mosquitto-clients
				mosquitto_pub -h cloud_mosquitto -m "Testing message throgh client" -t "facedetection_topic"
				
			vi) The topic name is "facedetection_topic"
				
	b) Another component will need to be created here to receive these binary files and save them to SoftLayer's Object storage
		i) Once the message in received in the cloud it should be saved in S3
		
		
		pip install ibm-cos-sdk
		
		
		 


docker run --name subscriber --network hw03  -ti cloud_forwarder 	

docker run --name cloud_mosquitto --network hw03  -ti cloud_mosquitto	
