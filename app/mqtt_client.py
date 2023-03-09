from paho.mqtt import client as mqtt_client
import time
class MQTTClient:

    # Connection Settings
    CLIENT_ID = 'Backend-Worker'
    # authentication
    # USERNAME = 'user'
    # PASSWORD = 'password'

    def __init__(self, broker_address, port, mongodb):
        print('init')
        self.client = self.connect_mqtt(broker_address, port)
        self.mongodb = mongodb

    # Connect to mqtt and return a MQTT Client object
    def connect_mqtt(self, broker_address, port):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        client = mqtt_client.Client(self.CLIENT_ID)
        # client.username_pw_set(username=, password)
        client.on_connect = on_connect
        client.connect(broker_address, port)
        return client

    # publish to a topic
    def publish(self, client, topic):
        msg_count = 0
        while True:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1

    # subscribes to a topic, with a MQTT Client attaches callback to process received messages
    def subscribe(self, topic, callback):
        # callback for processing received messages from the subscribed topic
        # self.client.loop_start()
        self.client.subscribe(topic)
        self.client.on_message = callback
        # TODO; Figure out loop, right now this command is blocking
        self.client.loop_forever()

    def force_start(self):
        self.client.loop_start()

    def force_stop(self):
        self.client.loop_stop()