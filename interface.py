from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import paho.mqtt.client as mqtt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


def publish_on(topic):
    client.publish("/etsidi/" + topic, "on", 0, True)


def publish_off(topic):
    client.publish("/etsidi/" + topic, "off", 0, True)


def pub_callbacks():
    ac1.pub_callback()
    ac2.pub_callback()
    ac3.pub_callback()
    ac4.pub_callback()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("/etsidi/humH")
    client.subscribe("/etsidi/tmpH")
    client.subscribe("/etsidi/ldrH")


def on_message(client, userdata, message):
    if message.topic == "/etsidi/humH":
        plot_msg(message, ax1, canvas1, (0, 100))
    if message.topic == "/etsidi/tmpH":
        plot_msg(message, ax2, canvas2, (-10, 50))
    if message.topic == "/etsidi/ldrH":
        plot_msg(message, ax3, canvas3, (0, 16000))


def plot_msg(message, axis, canvas, limits):

    # Read data
    data = str(message.payload.decode("utf-8"))
    print(message.topic, data)
    dataStr = data.split("_")
    dataNum = [int(num) for num in dataStr]
    ydata = dataNum
    xdata = [i for i in range(0, len(ydata))]

    # Clear previous graphics
    axis.clear()

    # Update lines
    line, = axis.plot(xdata, ydata, 'ro')
    line2, = axis.plot(xdata, ydata, 'k')
    line.set_xdata(xdata)
    line.set_ydata(ydata)
    line2.set_xdata(xdata)
    line2.set_ydata(ydata)

    # Set graph limits
    axis.set_xlim(0, len(ydata) - 1)
    axis.set_ylim(limits)

    # Display canvas
    canvas.show()


def on_window_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        global f_loop
        f_loop = False


class Actuator:

    def __init__(self, row, name, topic, fun_on, fun_off):

        self.topic = topic
        # On and off functions
        self.fun_on = fun_on
        self.fun_off = fun_off
        self.status = "off"

        # Actuator 1 text frame
        self.frame_text = Frame(actuators, borderwidth=1, relief=SUNKEN)
        self.frame_text.grid(column=1, row=row, rowspan=1, sticky=N + E + W + S)
        self.frame_text.rowconfigure(1, weight=1)
        self.frame_text.columnconfigure(1, weight=1)
        self.frame_text.columnconfigure(2, weight=1)
        # Actuator 1 text
        self.name_label = Label(self.frame_text, text=name, justify=LEFT)
        self.name_label.configure(font=("Arial", 12))
        self.name_label.grid(column=1, row=1, sticky=N+S+W, padx=2, pady=2)
        # Actuator 1 status
        self.status_label = Label(self.frame_text, text='inactive', justify=LEFT, bg="red")
        self.status_label.configure(font=("Arial", 12))
        self.status_label.grid(column=2, row=1, sticky=N+S+E, padx=2, pady=2)

        # Actuator 1 button frame
        self.frame_buttons = Frame(actuators, borderwidth=1, relief=SUNKEN)
        self.frame_buttons.grid(column=2, row=row, rowspan=1, sticky=N + E + W + S)
        self.frame_buttons.columnconfigure(1, weight=1)
        self.frame_buttons.columnconfigure(2, weight=1)
        # Actuator 1 start button
        self.button_on = Button(self.frame_buttons, text='Start', command=self.button_on)
        self.button_on.grid(column=1, row=1, sticky=W, padx=2, pady=2)
        # Actuator 1 stop button
        self.button_off = Button(self.frame_buttons, text='Stop', command=self.button_off)
        self.button_off.grid(column=2, row=1, sticky=E, padx=2, pady=2)

    def button_on(self):
        self.status_label.config(bg='green')
        self.status_label.config(text='active')
        self.status = "on"
        self.fun_on(self.topic)

    def button_off(self):
        self.status_label.config(bg='red')
        self.status_label.config(text='inactive')
        self.status = "off"
        self.fun_off(self.topic)

    def pub_callback(self):
        if self.status == "on":
            self.fun_on(self.topic)
        else:
            self.fun_off(self.topic)


# Set up Mosquitto client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("iot.eclipse.org", 1883, 60)

# Set up tkinter interface window
root = tk.Tk()
root.title("marvinApp")
w = 500
h = 500
root.minsize(w, h)
root.protocol("WM_DELETE_WINDOW", on_window_close)


# Main frame
mainframe = ttk.Frame(root, padding="15 15 15 15", borderwidth=4, relief=SUNKEN)
mainframe.grid(column=0, row=0, sticky=N+S+E+W)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.rowconfigure(1, weight=1)


# Graph frame
graph_frame = ttk.Frame(mainframe, padding="2 2 2 2", borderwidth=1, relief=SUNKEN)
graph_frame.grid(column=1, row=1, sticky=N+S+W)
graph_frame.columnconfigure(1, weight=1)
graph_frame.rowconfigure(1, weight=1)
graph_frame.rowconfigure(2, weight=1)
graph_frame.rowconfigure(3, weight=1)


# Figure 1 frame
fig1_frame = ttk.Frame(graph_frame)
fig1_frame.grid(column=1, row=1, sticky=N+E+W)
fig1_frame.rowconfigure(1, weight=1)
fig1_frame.rowconfigure(2, weight=1)

# Set up figure 1: humidity
fig1 = Figure(figsize=(3, 1.5))
ax1 = fig1.add_axes([0.15, 0.15, 0.8, 0.8])
canvas1 = FigureCanvasTkAgg(fig1, master=fig1_frame)
canvas1.get_tk_widget().grid(column=1, row=1, sticky=N, padx=2, pady=0)

# Caption for figure 1
cap1 = tk.Label(fig1_frame, text='Humedad (%)')
cap1.grid(column=1, row=2, sticky=N, padx=10, pady=5)


# Figure 2 frame
fig2_frame = ttk.Frame(graph_frame)
fig2_frame.grid(column=1, row=2, sticky=N+E+W)
fig2_frame.rowconfigure(1, weight=1)
fig2_frame.rowconfigure(2, weight=1)

# Set up figure 2: temperature
fig2 = Figure(figsize=(3, 1.5))
ax2 = fig2.add_axes([0.15, 0.15, 0.8, 0.8])
canvas2 = FigureCanvasTkAgg(fig2, master=fig2_frame)
canvas2.get_tk_widget().grid(column=1, row=1, sticky=N, padx=2, pady=0)

# Caption for figure 2
cap2 = tk.Label(fig2_frame, text='Temperatura (ºC)')
cap2.grid(column=1, row=2, sticky=N, padx=10, pady=5)


# Figure 3 frame
fig3_frame = ttk.Frame(graph_frame)
fig3_frame.grid(column=1, row=3, sticky=N+E+W)
fig3_frame.rowconfigure(1, weight=1)
fig3_frame.rowconfigure(2, weight=1)

# Set up figure 3: light level
fig3 = Figure(figsize=(3, 1.5))
ax3 = fig3.add_axes([0.18, 0.15, 0.8, 0.8])
canvas3 = FigureCanvasTkAgg(fig3, master=fig3_frame)
canvas3.get_tk_widget().grid(column=1, row=1, sticky=N, padx=2, pady=0)

# Caption for figure 3
cap3 = tk.Label(fig3_frame, text='Nivel de luz', pady=5)
cap3.grid(column=1, row=2, sticky=N, padx=10, pady=5)


# Info frame
info_frame = Frame(mainframe, borderwidth=1, relief=SUNKEN)
info_frame.grid(column=2, row=1, rowspan=1, sticky=N+E+W+S)
info_frame.columnconfigure(1, weight=1)
# info_frame.rowconfigure(2, weight=1)

# Top bar frame
top_bar = Frame(info_frame, borderwidth=1, relief=SUNKEN)
top_bar.grid(column=1, row=1, rowspan=1, sticky=N+E+W)

# Top bar: title
text1 = Label(top_bar, text='Supreme Funicular', justify=LEFT)
text1.configure(font=("Arial", 30))
text1.grid(column=1, row=1, sticky=N+W, padx=10, pady=4)

# Top bar: by
text1 = Label(top_bar, text='by cheriperi and juakofz', justify=LEFT)
text1.configure(font=("Arial", 12))
text1.grid(column=1, row=2, sticky=N+W, padx=10, pady=2)


# Actuators frame
actuators = Frame(info_frame)
actuators.grid(column=1, row=2, rowspan=1, sticky=N+S+E+W)
actuators.columnconfigure(1, weight=1)
for i in range(5):
    actuators.rowconfigure(i, weight=1)

# Actuators
ac1 = Actuator(1, "Water pump", "water", publish_on, publish_off)
ac2 = Actuator(2, "Fan", "fan", publish_on, publish_off)
ac3 = Actuator(3, "Cover", "cover", publish_on, publish_off)
ac4 = Actuator(4, "Lights", "lights", publish_on, publish_off)


# Main loop
c = 0
f_loop = True
while f_loop:

    # Client loop is too slow
    c += 1
    if c >= 10000:
        c = 0
        pub_callbacks()
        client.loop()

    root.update()


