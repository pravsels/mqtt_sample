import paho.mqtt.client as mqtt_cli
from random import uniform
import time

mqtt_broker = "mqtt.eclipseprojects.io"
client = mqtt_cli.Client("Temperature_Outside")
client.connect(mqtt_broker)

while True:
    number = uniform(10, 15)

    client.publish("temperature", number)

    print("Just published " + str(number) + " to Topic temperature")

    time.sleep(1)
