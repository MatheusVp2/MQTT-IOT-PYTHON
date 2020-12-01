import logging, eventlet, json
from flask import Flask, render_template, jsonify, request
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from pprint import pprint

from config import getDataDevice

eventlet.monkey_patch()

app = Flask(__name__, static_folder='./templates/src')

CORS(app)
cors = CORS(app, resources={
	r"/*": {
		"origins" : "*"
	}
})

#app.config['SECRET'] = 'my secret key'
#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '198.199.123.83'
# app.config['MQTT_BROKER_URL'] = 'broker.mqttdashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
app.config['MQTT_CLIENT_ID'] = 'admin:admin'
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_USERNAME'] = 'admin'
app.config['MQTT_PASSWORD'] = 'admin'
app.config['MQTT_KEEPALIVE'] = 10
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = '/admin/deb8e7/attrs'
app.config['MQTT_LAST_WILL_MESSAGE'] = ''
app.config['MQTT_LAST_WILL_QOS'] = 0

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt      = Mqtt(app)
socketio  = SocketIO(app)
bootstrap = Bootstrap(app)

subs_list = []

# Rotdas do Flask e API
@app.route('/')
def dash():
	return render_template('dash.html')

# Rotdas do Flask e API
@app.route('/msg')
def index():
	return render_template('index.html')

@app.route( '/device/<string:device>/attr/<string:attrs>', methods = ['GET'] )
def device_attr_info(device, attrs):
	# ENDPOINT -> /device/a68745/attr/geo
	return jsonify( getDataDevice( device, attrs ) )


# Logica para o Scoket Io
@socketio.on('publish')
def handle_publish(json_str):
	print("\n==================== ENVIANDO DATA ====================")
	print("JSON => {}".format(json_str) )

	data = json.loads(json_str)
	mqtt.publish( data['topic'] , json.dumps( data['message'] ) , data['qos'] )


@socketio.on('subscribe')
def handle_subscribe(json_str):
	print("\n==================== ATIVANDO DATA ====================")
	print("JSON => {}".format(json_str) )

	subs_list.append(json_str)

	data = json.loads(json_str)
	mqtt.subscribe( data['topic'], data['qos'] )


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
	print("\n==================== SAINDO GERAL ====================")
	if subs_list != []:
		mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	data = dict(
		topic=message.topic,
		payload=message.payload.decode(),
		qos=message.qos,
	)

	print("\n==================== RECEBENDO DATA ====================")
	print("JSON => {}".format(data) )

	socketio.emit('mqtt_message', data=data)


# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
# 	# print(level, buf)
# 	pass


if __name__ == '__main__':
	socketio.run( app, host='127.0.0.1', port=5000, use_reloader=False, debug=True )
