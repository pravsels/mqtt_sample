import paho.mqtt.client as mqtt_cli
import time

def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))

mqtt_broker = "mqtt.eclipseprojects.io"
client = mqtt_cli.Client("Smartphone")
client.connect(mqtt_broker)

client.subscribe("cmnd/localbytes_plug/Power")
client.on_message = on_message
time.sleep(1)

client.loop_forever()
