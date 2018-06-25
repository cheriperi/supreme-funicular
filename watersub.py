import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


def on_connect(client1, userdata, flags, rc):
    print("Connected with result code" + str(rc))

    client.subscribe("/etsidi/water")


def on_message(client1, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    if str(message.payload.decode("utf-8")) == "on":
        GPIO.output(LEDPIN, True)
        pass
    else:
        GPIO.output(LEDPIN, False)
        pass

LEDPIN = 19
#
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEDPIN, GPIO.OUT)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

client.loop_forever()
