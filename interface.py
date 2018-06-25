from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

last_hum = []
max_hum = 20
min_hum = 10

last_tmp = []
max_tmp = 35
min_tmp = 15

last_ldr = []
max_ldr = 15000
min_ldr = 5000

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
    print("Connected with result code: " + str(rc))
    client.subscribe("/etsidi/humH")
    client.subscribe("/etsidi/tmpH")
    client.subscribe("/etsidi/ldrH")


def on_message(client, userdata, message):
    if message.topic == "/etsidi/humH":
        global last_hum
        global max_hum
        global min_hum
        last_hum = plot_msg(message, ax1, canvas1, (0, 100), max_hum, min_hum, 'bo')
    if message.topic == "/etsidi/tmpH":
        global last_tmp
        global max_tmp
        global min_tmp
        last_tmp = plot_msg(message, ax2, canvas2, (-10, 50), max_tmp, min_tmp, 'bo')
    if message.topic == "/etsidi/ldrH":
        global last_ldr
        global max_ldr
        global min_ldr
        last_ldr = plot_msg(message, ax3, canvas3, (0, 16000), max_ldr, min_ldr, 'bo')


def plot_msg(message, axis, canvas, limits, max, min, color='ro'):

    # Read data
    data = str(message.payload.decode("utf-8"))
    print(message.topic, data)
    dataStr = data.split("_")
    dataNum = [int(num) for num in dataStr]
    ydata = dataNum
    xdata = [i for i in range(0, len(ydata))]
    last_var = ydata[-1]
    print(last_var)
    # Clear previous graphics
    axis.clear()

    # Update graph lines
    line, = axis.plot(xdata, ydata, color)
    line2, = axis.plot(xdata, ydata, 'k')
    line.set_xdata(xdata)
    line.set_ydata(ydata)
    line2.set_xdata(xdata)
    line2.set_ydata(ydata)

    # Update max/min area
    if last_var < min or last_var > max:
        c = 'r'
    else:
        c = 'g'

    axis.axhline(max, color=c, lw=1)
    axis.axhline(min, color=c, lw=1)
    axis.axhspan(min, max, facecolor=c, alpha=0.5)

    # Set graph limits
    axis.set_xlim(0, len(ydata) - 1)
    axis.set_ylim(limits)

    # Display canvas
    canvas.show()
    return last_var


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
        self.status_label = Label(self.frame_text, text='inactive', justify=LEFT, bg="red", padx=5)
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


class paramBox:

    def __init__(self, row, name, def_max, def_min, last_var):

        self.max = def_max
        self.min = def_min

        # Param main text frame
        self.frame_text = Frame(parameters, borderwidth=1, relief=SUNKEN)
        self.frame_text.grid(column=1, row=row, rowspan=1, sticky=N + E + W + S)
        self.frame_text.rowconfigure(1, weight=1)
        self.frame_text.rowconfigure(2, weight=1)
        self.frame_text.columnconfigure(1, weight=1)
        # self.frame_text.columnconfigure(2, weight=1)
        # Param text
        self.name_label = Label(self.frame_text, text=name, justify=LEFT)
        self.name_label.configure(font=("Arial", 12))
        self.name_label.grid(column=1, row=1, columnspan=2, sticky=N + S + W, padx=2, pady=2)
        # Value
        self.value_label = Label(self.frame_text, text=last_var, justify=LEFT)
        self.value_label.configure(font=("Arial", 12))
        self.value_label.grid(column=1, row=2, rowspan=1, sticky=N + S + W, padx=2, pady=2)
        # Actuator 1 status
        self.status_label = Label(self.frame_text, text='ok', justify=LEFT, bg="green", padx=5)
        self.status_label.configure(font=("Arial", 12))
        self.status_label.grid(column=2, row=2, sticky=N+S+W, padx=2, pady=2)

        # Param setup frame
        self.setup_frame = Frame(parameters, borderwidth=1, relief=SUNKEN)
        self.setup_frame.grid(column=2, row=row, sticky=N + W + S)
        self.setup_frame.rowconfigure(1, weight=1)
        self.setup_frame.rowconfigure(2, weight=1)
        self.setup_frame.columnconfigure(1, weight=1)
        self.setup_frame.columnconfigure(2, weight=1)
        self.setup_frame.columnconfigure(3, weight=1)

        # Max text
        self.max_label = Label(self.setup_frame, text="Max", justify=LEFT)
        self.max_label.configure(font=("Arial", 12))
        self.max_label.grid(column=1, row=1, rowspan=1, sticky=N + S + W, padx=2, pady=2)
        # Max entry
        self.max_entry = Entry(self.setup_frame, bd=2)
        self.max_entry.grid(column=2, row=1, rowspan=1, sticky=N + S + W, padx=2, pady=2)
        self.max_entry.insert(END, def_max)
        # Max set button
        self.button_max = Button(self.setup_frame, text='Set', command=self.set_max)
        self.button_max.grid(column=3, row=1, sticky=E, padx=2, pady=2)

        # Min text
        self.min_label = Label(self.setup_frame, text="Min", justify=LEFT)
        self.min_label.configure(font=("Arial", 12))
        self.min_label.grid(column=1, row=2, rowspan=1, sticky=N + S + W, padx=2, pady=2)
        # Min entry
        self.min_entry = Entry(self.setup_frame, bd=2)
        self.min_entry.grid(column=2, row=2, rowspan=1, sticky=N + S + W, padx=2, pady=2)
        self.min_entry.insert(END, def_min)
        # Min set button
        self.button_min = Button(self.setup_frame, text='Set', command=self.set_min)
        self.button_min.grid(column=3, row=2, sticky=E, padx=2, pady=2)

    def update(self, last_var):
        self.value_label.config(text=last_var)
        if not last_var:
            self.status_label.config(bg='yellow')
            self.status_label.config(text='no value')
        elif last_var > self.max or last_var < self.min:
            self.status_label.config(bg='red')
            self.status_label.config(text='not ok')
        else:
            self.status_label.config(bg='green')
            self.status_label.config(text='ok')
        return self.max, self.min

    def set_max(self):
        self.max = int(self.max_entry.get())

    def set_min(self):
        self.min = int(self.min_entry.get())



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
mainframe = tk.Frame(root, padx=15, pady=15, borderwidth=4, relief=SUNKEN)
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
fig1_frame = tk.Frame(graph_frame, bg="white")
fig1_frame.grid(column=1, row=1, sticky=N+E+W)
fig1_frame.rowconfigure(1, weight=1)
fig1_frame.rowconfigure(2, weight=1)

# Set up figure 1: humidity
fig1 = Figure(figsize=(3, 1.5))
ax1 = fig1.add_axes([0.15, 0.15, 0.8, 0.8])
canvas1 = FigureCanvasTkAgg(fig1, master=fig1_frame)
canvas1.get_tk_widget().grid(column=1, row=1, sticky=N, padx=2, pady=0)

# Caption for figure 1
cap1 = tk.Label(fig1_frame, text='Humidity (%)')
cap1.grid(column=1, row=2, sticky=N, padx=10, pady=5)


# Figure 2 frame
fig2_frame = tk.Frame(graph_frame, bg="white")
fig2_frame.grid(column=1, row=2, sticky=N+E+W)
fig2_frame.rowconfigure(1, weight=1)
fig2_frame.rowconfigure(2, weight=1)

# Set up figure 2: temperature
fig2 = Figure(figsize=(3, 1.5))
ax2 = fig2.add_axes([0.15, 0.15, 0.8, 0.8])
canvas2 = FigureCanvasTkAgg(fig2, master=fig2_frame)
canvas2.get_tk_widget().grid(column=1, row=1, sticky=N, padx=2, pady=0)

# Caption for figure 2
cap2 = tk.Label(fig2_frame, text='Temperature (ºC)')
cap2.grid(column=1, row=2, sticky=N, padx=10, pady=5)


# Figure 3 frame
fig3_frame = tk.Frame(graph_frame, bg="white")
fig3_frame.grid(column=1, row=3, sticky=N+E+W)
fig3_frame.rowconfigure(1, weight=1)
fig3_frame.rowconfigure(2, weight=1)

# Set up figure 3: light level
fig3 = Figure(figsize=(3, 1.5))
ax3 = fig3.add_axes([0.18, 0.15, 0.8, 0.8])
canvas3 = FigureCanvasTkAgg(fig3, master=fig3_frame)
canvas3.get_tk_widget().grid(column=1, row=1, sticky=N, padx=2, pady=0)

# Caption for figure 3
cap3 = tk.Label(fig3_frame, text='Light level')
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
actuators.grid(column=1, row=2, rowspan=1, sticky=N+E+W)
actuators.columnconfigure(1, weight=1)
for i in range(5):
    actuators.rowconfigure(i, weight=1)

# Actuators title
actuators_title = Label(actuators, text='Actuators', justify=LEFT)
actuators_title.configure(font=("Arial", 20))
actuators_title.grid(column=1, row=1, columnspan=2, sticky=N+S+E+W, padx=10, pady=5)

# Actuators
ac1 = Actuator(2, "Water pump", "water", publish_on, publish_off)
ac2 = Actuator(3, "Fan", "fan", publish_on, publish_off)
ac3 = Actuator(4, "Cover", "cover", publish_on, publish_off)
ac4 = Actuator(5, "Lights", "lights", publish_on, publish_off)

# Parameters frame
parameters = Frame(info_frame)
parameters.grid(column=1, row=3, rowspan=1, sticky=N+S+E+W)
parameters.columnconfigure(1, weight=2)
parameters.columnconfigure(2, weight=1)
for i in range(5):
    parameters.rowconfigure(i, weight=1)

# Parameters title
param_title = Label(parameters, text='Parameters', justify=LEFT)
param_title.configure(font=("Arial", 20))
param_title.grid(column=1, row=1, columnspan=2, sticky=N+S+E+W, padx=10, pady=5)


p1 = paramBox(2, "Humidity", max_hum, min_hum, last_hum)
p2 = paramBox(3, "Temperature", max_tmp, min_tmp, last_tmp)
p3 = paramBox(4, "Light", max_ldr, min_ldr, last_ldr)


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

    max_hum, min_hum = p1.update(last_hum)
    max_tmp, min_tmp = p2.update(last_tmp)
    max_ldr, min_ldr = p3.update(last_ldr)
    root.update()


