import matplotlib.pyplot as ptl
import paho.mqtt.client as mqtt
import time

def on_connect(client1, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	
	client.subscribe("/etsidi/humH")
	
def on_message(client1, userdata, message):
	data = str(message.payload.decode("utf-8"))
	print("message received ", data)

	dataStr = data.split("_")
	dataNum = [int(num) for num in dataStr]
	ydata = dataNum	
	#ptl.plot(dataNum, 'ro')
	#ptl.show()
	axes.set_xlim(0, len(ydata) - 1)
	axes.set_ylim(0, 100)
	xdata = [i for i in range(0, len(ydata))]
	
	line.set_xdata(xdata)
	line.set_ydata(ydata)
	
	line2.set_xdata(xdata)
	line2.set_ydata(ydata)
	
	ptl.draw()
	ptl.pause(1e-17)
	time.sleep(0.1)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

xdata = []
ydata = []
ptl.show()
axes = ptl.gca()
axes.set_xlim(0, 100)
axes.set_ylim(0, 100)
line, = axes.plot(xdata, ydata, 'ro')
line2, = axes.plot(xdata, ydata, 'k')

client.loop_forever()
