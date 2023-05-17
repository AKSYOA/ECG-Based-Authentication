from tkinter import *
from tkinter import filedialog
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from App.Data_Preparation import load_signal, filter_signal, segment_signal

root = Tk()
root.title("Signature Identification and Verification")
root.configure(background='white')
root.geometry("1000x800")

root.filename = filedialog.askopenfilename(title="Select a file")

# Read Signal
signal, fields = load_signal(root.filename[0:-4])

# plot Signal on GUI
fig = Figure(figsize=(6, 4))
ax = fig.add_subplot(111)
ax.plot(signal)
ax.set_title('ECG Signal')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.set_xlim(3000, 6000)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, expand=1)
canvas.get_tk_widget().configure(width=1000, height=400)
canvas.draw()

start = 3000
end = 6000
iterations = 0


def once():
    global iterations
    global start, end
    ax.clear()
    ax.plot(signal)
    ax.set_xlim(start + 50, end + 50)

    start += 50
    end += 50

    canvas.draw()
    iterations += 1

    # Schedule the next plot update after a specified interval (e.g., 1000 milliseconds)
    if iterations < 6000:
        root.after(100, once)


once()
# Extract Features from signal depend on Type
filtered_signal = filter_signal(signal)
segments = segment_signal(filtered_signal)
mainloop()
