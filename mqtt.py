import paho.mqtt.client as mqtt
import json
import time

#
# Properties definition
host_mqtt   = "198.199.123.83"
port_mqtt   = 1883
tenant_name = "admin"
device_id   = "a68745"

#
# Internal definitions setup
client_id = "{}:{}".format(tenant_name, device_id)

topic_to_publish = "/{}/{}/attrs".format(tenant_name, device_id)
topic_to_subscribe = "/{}/{}/config".format(tenant_name, device_id)

def on_message(client, userdata, message):
	data = dict(
		topic=message.topic,
		payload=message.payload.decode(),
		qos=message.qos,
	)
	retorno = json.loads( data['payload'] )
	print("Received", retorno)
	try:
		if retorno['porta']:
			print("Abrindo Porta !")
			print("Abrindo Porta !")
			print("Abrindo Porta !")
			message = {
				"porta" : False
			}
			print("Publishing", message, 'to topic', topic_to_publish)
			client.publish(topic_to_publish, json.dumps(message))
	except Exception as e:
		pass

def on_connect( client, userdata, flags, rc ):
	print("Conectado a : ", str(rc) )
	print("Subscribing to topic", topic_to_subscribe)
	client.subscribe(topic_to_subscribe)


#
# MQTT Client setup and connection
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to mqtt broker")
client.connect( host=host_mqtt, port=port_mqtt )

client.loop_forever()
