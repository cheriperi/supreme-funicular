import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


def on_connect(client1, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	
	client.subscribe("/etsidi/ldr")
	
def on_message(client1, userdata, message):
	print("message received ", str(message.payload.decode("utf-8")))
	if int(message.payload) >= 2500:
		GPIO.output(LEDPIN, True)
	else:
		GPIO.output(LEDPIN, False)

LEDPIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEDPIN, GPIO.OUT)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

client.loop_forever()
