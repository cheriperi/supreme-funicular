
import paho.mqtt.client as mqtt #import the client
import RPi.GPIO as GPIO
import time

def on_connect(client, userdata, flags, rc):
	m="Connected flags: " + str(flags) + " result code: " + str(rc) + " client1_id: " + str(client)
	print(m)

def rc_time(LDRPIN):
	count = 0
	GPIO.setup(LDRPIN, GPIO.OUT)
	GPIO.output(LDRPIN, GPIO.LOW)
	time.sleep(0.1)
	
	GPIO.setup(LDRPIN, GPIO.IN)
	
	while (GPIO.input(LDRPIN) == GPIO.LOW):
		count += 1
		#print(str(count))
		
	return count
	
LDRPIN = 15
GPIO.setmode(GPIO.BCM)

broker_address="iot.eclipse.org"
client=mqtt.Client()
client.on_connect=on_connect
client.connect(broker_address, 1883, 60)
client.loop_start()

while True:
	val = rc_time(LDRPIN)
	print("rc time = " + str(val))
	client.publish("/etsidi/ldr", val, 0, True)


client.disconnect()
client.loop_stop()
