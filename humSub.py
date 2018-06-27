import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

threshold = 40

def on_connect(client1, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	
	client.subscribe("/etsidi/hum")
	client.subscribe("/etsidi/params")
	
def on_message(client1, userdata, message):
	global threshold
	print("message received ", str(message.payload.decode("utf-8")))
	if message.topic == "/etsidi/hum":
		if int(message.payload) >= threshold:
			GPIO.output(LEDPIN, True)
			print("Value higher that threshold")
		else:
			GPIO.output(LEDPIN, False)
	if message.topic == "/etsidi/params":
		data = str(message.payload.decode("utf-8"))
		dataStr = data.split("_")
		dataNum = [int(num) for num in dataStr]
		threshold = dataNum[0]
		print("Changed threshold to " + str(threshold))
		
		

LEDPIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEDPIN, GPIO.OUT)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

client.loop_forever()
