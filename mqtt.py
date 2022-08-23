
import logging
from paho.mqtt import client as mqtt_client
import time

client_id = 'python-mqtt-2'


def connect_mqtt(mqtt_host, mqtt_port, mqtt_user, mqtt_password):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(mqtt_user, mqtt_password)
    client.on_connect = on_connect
    client.connect(mqtt_host, mqtt_port)
    return client


def publish(client, topic, msg):

    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        logging.info(f"Send `{msg}` to topic `{topic}`")
    else:
        logging.info(f"Failed to send message to topic {topic}")


def run(mqtt_host, mqtt_port, mqtt_user, mqtt_password, topic, msg):
    client = connect_mqtt(mqtt_host, mqtt_port, mqtt_user, mqtt_password)
    client.loop_start()
    publish(client, topic, msg)
