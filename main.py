import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

int tpm_value
int hum_value
int ldr_value

def on_connect(client1, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	
	client.subscribe(["/etsidi/tmp", "/etsidi/hum", "/etsidi/ldr"], [0,0,0])
	
def on_message(client1, userdata, message):
	print("message received ", str(message.payload.decode("utf-8")), "topic", message.topic)

	# Read and update temperature values
	if message.topic == "/etsidi/tmp"
		tpm_value = int(message.payload)

	# Read and update humidity values
	if message.topic == "/etsidi/hum"
		hum_value = int(message.payload)

	# Read and update light values
	if message.topic == "/etsidi/ldr"
		ldr_value = int(message.payload)

LEDPIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEDPIN, GPIO.OUT)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.message_callback_add(sub, callback)
client.message_callback_add(sub, callback)
client.message_callback_add(sub, callback)

client.connect("iot.eclipse.org", 1883, 60)

client.loop_forever()
