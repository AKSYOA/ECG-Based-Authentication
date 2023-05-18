import tkinter as tk
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk, ImageSequence
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from App.Data_Preparation import load_signal
from Interface.Run import run

root = Tk()
root.title("Signature Identification and Verification")
root.configure(background='gray')
root.resizable(False, False)
root.geometry("1000x600")

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

# People on the system
Users = {0: "Salem", 1: "Mohamed", 2: "Ali", 3: "Fathy"}

# Create another container for everything but signal plot
container2 = tk.Frame(root, bg="white")
container2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Choose Feature Extraction method
feature_extraction_method_value = IntVar()
Label(container2, text='Feature Extraction Method', background='white', font=("Helvetica", 16)).grid(row=1, column=0,
                                                                                                     pady=30)

Fiducial_radio_button = Radiobutton(container2, text="Fiducial", variable=feature_extraction_method_value, value=1,
                                    font=("Helvetica", 16), background='white', bd=0, relief=tk.RAISED,
                                    highlightthickness=0)
Fiducial_radio_button.grid(row=1, column=1, padx=10)

Non_fiducial_radio_button = Radiobutton(container2, text="Non-Fiducial", variable=feature_extraction_method_value,
                                        value=2,
                                        font=("Helvetica", 16), background='white', bd=0, relief=tk.RAISED,
                                        highlightthickness=0)
Non_fiducial_radio_button.grid(row=1, column=2, padx=10)

gif_image = Image.open("../assets/unlocked.gif")
frames = []

for i in ImageSequence.Iterator(gif_image):
    frames.append(ImageTk.PhotoImage(i))
print(len(frames))


def update_frame(index):
    frame = frames[index]
    tk.Label(container2, image=frame, bd=0, highlightthickness=0).grid(row=3, column=5)
    if index + 1 < len(frames):
        container2.after(50, update_frame, (index + 1))


# Login button
def execute():
    person_index = run(signal, feature_extraction_method_value.get())
    if person_index == -1:  # which is impossible
        Label(container2, text='You are not Authorized', background='white', font=("Helvetica", 16)).grid(row=3,
                                                                                                          column=2,
                                                                                                          pady=30)
    else:
        message = 'Welcome back, {name}'.format(name=Users[person_index])
        Label(container2, text=message, background='white', font=("Helvetica", 16)).grid(row=3,
                                                                                         column=2,
                                                                                         pady=30)
        update_frame(20)


Button(container2, text='Login', width=10, font=("Helvetica", 16), command=execute).grid(row=2, column=2, padx=30)

# unlocked gif


mainloop()
