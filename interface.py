from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import matplotlib.pyplot as ptl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import time


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
        plot_msg(message, ax3, canvas3, (0, 15000))


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
    #canvas.get_tk_widget().pack()


def on_window_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        global f_loop
        f_loop = False


# Set up Mosquitto client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("iot.eclipse.org", 1883, 60)

# Set up tkinter interface window
root = tk.Tk()
root.title("marvinApp")
w = 800
h = 550
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


# Frame 1: top bar
top_bar = Frame(mainframe, borderwidth=1, relief=SUNKEN)
top_bar.grid(column=2, row=1, rowspan=1, sticky=N+E+W)

# Frame 1.1: title
text1 = Label(top_bar, text='Supreme Funicular', justify=LEFT)
text1.configure(font=("Arial", 30))
text1.grid(column=1, row=1, sticky=N+W, padx=10, pady=4)

# Main loop
f_loop = True
while f_loop:
    print("looping")
    client.loop()
    root.update()


