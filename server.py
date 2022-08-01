from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

plug_data = {"topic": "", "payload": ""}

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = "mqtt.eclipseprojects.io"  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('stat/localbytes_plug/POWER')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    plug_data["topic"] = message.topic
    plug_data["payload"] = message.payload.decode()


@app.route('/toggle', methods=['GET'])
def toggle():
    # publish_result = mqtt.publish("cmnd/localbytes_plug/Power", "TOGGLE")
    publish_result = mqtt.publish("cmnd/localbytes_plug/Power", "TOGGLE")

    return jsonify({'status': publish_result[0]})


@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': plug_data["payload"]})


if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)
