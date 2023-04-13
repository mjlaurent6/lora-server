from paho.mqtt import client as mqtt_client
import json
import time

# class for MQTT operations
class MQTTClient():

    # Connection Settings
    CLIENT_ID = 'Backend-Worker'
    # authentication
    # USERNAME = 'user'
    # PASSWORD = 'password'

    def __init__(self, broker_address, port):
        self.broker_address = broker_address
        self.port = port

    # Connect to mqtt and return a MQTT Client object
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        def on_disconnect(client, userdata, rc):
            print("Disconnect")
        # Set Connecting Client ID
        client = mqtt_client.Client(self.CLIENT_ID)
        # client.username_pw_set(username=, password)
        # client.on_connect = on_connect
        # client.on_disconnect = on_disconnect
        client.connect(self.broker_address, self.port)
        return client

    # publish a message to a topic
    def publish(self, topic: str, msg: str):
        client = self.connect_mqtt()
        print(msg)
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        client.disconnect()

    # subscribe and waits 
    def sub_and_wait(self, topic, timeout):
        stop = False
        # connect to mqtt
        client = self.connect_mqtt()
        response = None
        def on_message(client, userdata, msg):
            nonlocal stop
            nonlocal response
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

            response = msg
            stop = True

        client.subscribe(topic)
        client.on_message = on_message
        start_time = time.time()
        
        elapsed_time = 0
        # loop for the alloted time or when message has been received
        while elapsed_time < timeout and not stop:
            client.loop()
            elapsed_time = time.time() - start_time
        client.loop_stop()
        client.unsubscribe(topic)
        # disconnect 
        client.disconnect()
        
        return response, elapsed_time

        