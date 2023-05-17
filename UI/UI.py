from tkinter import *
from tkinter import filedialog

from App.Data_Preparation import load_signal, filter_signal, segment_signal

root = Tk()
root.title("Signature Identification and Verification")
root.configure(background='white')
root.geometry("600x600")

root.filename = filedialog.askopenfilename(title="Select a file")

# Read Signal
signal, fields = load_signal(root.filename[0:-4])

# plot Signal on GUI


# Extract Features from signal depend on Type
filtered_signal = filter_signal(signal)
segments = segment_signal(filtered_signal)
