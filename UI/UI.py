from tkinter import *
from tkinter import filedialog
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from App.Data_Preparation import load_signal, filter_signal, segment_signal

root = Tk()
root.title("Signature Identification and Verification")
root.configure(background='gray')
root.geometry("1000x800")

root.filename = filedialog.askopenfilename(title="Select a file")

# Read Signal
signal, fields = load_signal(root.filename[0:-4])

# plot Signal on GUI
fig = Figure(figsize=(6, 4))
ax = fig.add_subplot(111)
ax.plot(signal)
ax.set_xlim(0, 3000)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
canvas.get_tk_widget().configure(width=1000, height=300)
canvas.draw()

start = 0
end = 3000
iterations = 0


def update_plot():
    global iterations
    global start, end
    ax.clear()
    ax.plot(signal)
    ax.set_xlim(start + 100, end + 100)

    start += 100
    end += 100

    canvas.draw()
    iterations += 1

    # Schedule the next plot update after a specified interval (e.g., 1000 milliseconds)
    if iterations < 6000:
        root.after(20, update_plot)


update_plot()

# Create another container for everything but signal plot
container2 = tk.Frame(root, bg="white")
container2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Choose Feature Extraction method
feature_extraction_method_value = IntVar()
Label(container2, text='Feature Extraction Method', background='white', font=("Helvetica", 16)).grid(row=1, column=0,
                                                                                                     pady=30)

Fiducial_radio_button = Radiobutton(container2, text="Fiducial", variable=feature_extraction_method_value, value=1,
                                    font=("Helvetica", 16), background='white', bd=2, relief=tk.RAISED)
Fiducial_radio_button.grid(row=1, column=1, padx=10)

Non_fiducial_radio_button = Radiobutton(container2, text="Non-Fiducial", variable=feature_extraction_method_value,
                                        value=2,
                                        font=("Helvetica", 16), background='white', bd=2, relief=tk.RAISED)
Non_fiducial_radio_button.grid(row=1, column=2, padx=10)


# Login button
def run():
    pass
    # filtered_signal = filter_signal(signal)
    # segments = segment_signal(filtered_signal)


Button(container2, text='Login', width=10, font=("Helvetica", 16), command=run).grid(row=2, column=2, padx=30)

# Extract Features from signal depend on Type

mainloop()
