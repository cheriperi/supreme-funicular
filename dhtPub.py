
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
numData = 50
dataHumH = [0 for i in range(0, numData)]
dataTemH = [0 for i in range(0, numData)]

while True:
	result = read_dht11_dat()
	if result:
		humidity, temperature = result
		print ("humidity: ", humidity, "%, ", "Temperature: ", temperature, " C") 
		
		dataHumH.pop(0)
		dataHumH.append(humidity)
		dataHumHStr = "_".join(str(x) for x in dataHumH)
		
		print("hist data hum = " + dataHumHStr)
		client.publish("/etsidi/humH", dataHumHStr, 0, True)
		
		dataTemH.pop(0)
		dataTemH.append(temperature)
		dataTemHStr = "_".join(str(x) for x in dataTemH)
		
		print("hist data tmp = " + dataTemHStr)
		client.publish("/etsidi/tmpH", dataTemHStr, 0, True)
	
		client.publish("/etsidi/tmp", temperature, 0, True)
		client.publish("/etsidi/hum", humidity, 0, True)
	time.sleep(1)


client.disconnect()
client.loop_stop()
