
# publisher of the temperature and humidity

import RPi.GPIO as GPIO
import time
from dht11 import read_dht11_dat
import paho.mqtt.client as mqtt #import the client

def on_connect(client, userdata, flags, rc):
	m="Connected flags: " + str(flags) + " result code: " + str(rc) + " client1_id: " + str(client)
	print(m)
	
	
broker_address="iot.eclipse.org"
client=mqtt.Client()
client.on_connect=on_connect
client.connect(broker_address, 1883, 60)
client.loop_start()



while True:
	result = read_dht11_dat()
	if result:
		humidity, temperature = result
		print ("humidity: ", humidity, "%, ", "Temperature: ", temperature, " C") 
		client.publish("/etsidi/tmp", temperature, 0, True)
		client.publish("/etsidi/hum", humidity, 0, True)
	time.sleep(1)


client.disconnect()
client.loop_stop()
