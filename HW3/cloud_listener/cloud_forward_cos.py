import paho.mqtt.client as mqtt
import os
import uuid
import ibm_boto3
from ibm_botocore.client import Config
from ibm_botocore.exceptions import ClientError
import ibm_s3transfer.manager

#mosquito configuration
LOCAL_MQTT_HOST="cloud_mosquitto"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="cloud_facedetection_topic"


#Cloud Object Storage configuration
COS_ENDPOINT = "https://s3.us.cloud-object-storage.appdomain.cloud" # example: https://s3.us-south.cloud-object-storage.appdomain.cloud
COS_API_KEY_ID = "HYeXrcCwgxI96sI_gMQSBRsUkflIDl2UX9oROSGn_nOE" # example: xxxd12V2QHXbjaM99G9tWyYDgF_0gYdlQ8aWALIQxXx4
COS_AUTH_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"
COS_SERVICE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/242183bed8d743ab90c92a2dcaf3c3e8:3fb1c162-4d7e-4d40-a2e9-f502e63c0cb6::" # example: crn:v1:bluemix:public:cloud-object-storage:global:a/xx999cd94a0dda86fd8eff3191349999:9999b05b-x999-4917-xxxx-9d5b326a1111::
COS_STORAGE_CLASS = "us-standard" # example: us-south-standard
BUCKET_NAME="w251-aditi-bucket"

# Create client connection
cos_cli = ibm_boto3.client("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_SERVICE_CRN,
    ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

def log_done():
    print("DONE!\n")

def log_client_error(e):
    print("CLIENT ERROR: {0}\n".format(e))

def log_error(msg):
    print("UNKNOWN ERROR: {0}\n".format(msg))
  
def get_uuid():
    l = list(range(1, 1000))
    return str(l.pop(0))
        
def uploadToObjectStore(message):
	try:
		item_name = "face_" + get_uuid() + ".png"
    	cos_cli.put_object(
            Bucket=BUCKET_NAME,
            Key=item_name,
            Body=message
        )
        print("Item: {0} created!".format(item_name))
        log_done()
    except ClientError as be:
        log_client_error(be)
    except Exception as e:
        log_error("Unable to create text file: {0}".format(e))    
        
        
        
        
def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  try:
    print("message received!")	
    # if we wanted to re-publish this message, something like this should work
    msg = msg.payload
    print(msg) 
    #Upload the message to S3
    uploadToObjectStore(msg)
    
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message


# go into a loop
local_mqttclient.loop_forever()


        
        
        
        
        
        
        
        
        
        
        