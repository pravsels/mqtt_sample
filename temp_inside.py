import paho.mqtt.client as mqtt
from random import uniform
import time

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)

while True:
    number = uniform(20, 25)

    client.publish("temperature", number)

    print("Just published " + str(number) + " to Topic temperature")

    time.sleep(1)
