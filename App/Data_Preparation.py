import wfdb
from scipy.signal import butter, filtfilt
import numpy as np

fs = 1000.0
nyquist_rate = 0.5 * fs

order = 2
low = 1.0 / nyquist_rate
high = 40.0 / nyquist_rate


def load_signal(signal_path):
    signal, _ = wfdb.rdsamp(signal_path, channels=[1])
    return signal[96000:120012]


def filter_signal(signal):
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal[:, 0])


segment_length = 2000
overlap = 200


def segment_signal(signal):  # filtered_signal
    segments = []
    num_segments = int(np.ceil((len(signal) - segment_length) / overlap)) + 1

    for j in range(num_segments):
        start = j * overlap
        end = start + segment_length

        if end > len(signal):
            end = len(signal)
            start = end - segment_length

        segments.append(signal[start:end])
    return np.array(segments)
