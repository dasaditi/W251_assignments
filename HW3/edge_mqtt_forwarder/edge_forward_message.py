import paho.mqtt.client as mqtt

#mosquito configuration
LOCAL_MQTT_HOST="edge_mosquitto"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="edge_facedetection_topic"

#mosquito configuration
#CLOUD_MQTT_HOST="mqtt.eclipse.org"
CLOUD_MQTT_HOST="169.45.88.52"
CLOUD_MQTT_PORT=1883
CLOUD_MQTT_TOPIC="cloud_facedetection_topic"

def edge_on_connect(client, userdata, flags, rc):
    print("Connected to the edge MQTT with result code: " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(LOCAL_MQTT_TOPIC)

def cloud_on_connect(client, userdata, flags, rc):
    print("Connected to the cloud MQTT with result code: " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe(CLOUD_MQTT_TOPIC)


def edge_on_message(client, userdata, msg):
    try:
        print("Message received on " + msg.topic + ": " + str(msg.payload))
        print("Publishing message to the cloud...")
        pub_resp = cloud_client.publish(CLOUD_MQTT_TOPIC, msg.payload)
        print("Publish response: " + str(pub_resp))
    except:
        print("unexpected error")

def cloud_on_publish(client, userdata, result):
    print("Message published: " + str(result))


edge_client = mqtt.Client()
edge_client.on_connect = edge_on_connect
edge_client.on_message = edge_on_message
edge_client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

cloud_client = mqtt.Client()
cloud_client.on_connect = cloud_on_connect
cloud_client.on_publish = cloud_on_publish
cloud_client.connect(CLOUD_MQTT_HOST, CLOUD_MQTT_PORT, 60)

edge_client.loop_forever()
