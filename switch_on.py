import paho.mqtt.client as mqtt_cli
from random import uniform
import time

mqtt_broker = "mqtt.eclipseprojects.io"
client = mqtt_cli.Client("plug_client")
client.connect(mqtt_broker)

while True:

    client.publish("cmnd/localbytes_plug/Power", "TOGGLE")

    print("sent toggle command!")

    time.sleep(1)
