import numpy as np
import cv2
import base64
from datetime import datetime
import paho.mqtt.client as mqtt

#mosquito configuration
LOCAL_MQTT_HOST="edge_mosquitto"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="edge_facedetection_topic"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("faces/detect")

def on_publish(client, userdata, result):
    print("Message published: " + str(result))

# Load face classifier, video camera, and MQTT client
face_cascade = cv2.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Create gray image
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Check for faces
    faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
    face_count = len(faces)
    print("Found " + str(face_count) + " in this frame.")
    img = cv2.imshow('frame', gray_img)
    # Draw rectangle around face
    for (x,y,w,h) in faces:
        cv2.rectangle(gray_img, (x,y), (x+w, y+h), (255,0,0), 2)
    
    # Only send images with faces
    if face_count > 0:
        gray_jpg = cv2.imencode('.jpg', gray_img)[1]
        cv2.imwrite("face-"+str(datetime.now())+".jpg", gray_img)
        gray_text = base64.b64encode(gray_jpg)
        
        pub_resp = client.publish(LOCAL_MQTT_TOPIC, gray_text)
        print("Publish response: " + str(pub_resp))
        
        # Close the connection
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
# Time to wait next command, avoid blockage
time.sleep(1) 
        
# When everything is done, release the capture, stop the loop and disconnect from client
client.loop_stop()
client.disconnect()
cap.release()
cv2.destroyAllWindows()        






