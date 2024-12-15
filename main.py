import RPi.GPIO as GPIO
import time
import librosa
import numpy as np

def setup():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(2, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(10, GPIO.OUT)
    GPIO.setup(9, GPIO.OUT)

def output(values):

    GPIO.output(2, GPIO.HIGH if values[0] else GPIO.LOW)
    GPIO.output(3, GPIO.HIGH if values[1] else GPIO.LOW)
    GPIO.output(4, GPIO.HIGH if values[2] else GPIO.LOW)
    GPIO.output(17, GPIO.HIGH if values[3] else GPIO.LOW)
    GPIO.output(27, GPIO.HIGH if values[4] else GPIO.LOW)
    GPIO.output(22, GPIO.HIGH if values[5] else GPIO.LOW)
    GPIO.output(10, GPIO.HIGH if values[6] else GPIO.LOW)
    GPIO.output(9, GPIO.HIGH if values[7] else GPIO.LOW)

def teardown():
    GPIO.cleanup()

def loadAudio():
    file_path = "./happy-birthday-266285.mp3"
    y, sr = librosa.load(file_path)
    return y, sr

def dsp(y, sr):

    # Compute the Short-Time Fourier Transform (STFT)
    n_fft = 2048  # FFT window size
    hop_length = 512  # Number of samples between successive frames
    stft_matrix = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

    # Get the magnitude of the STFT (absolute value of complex numbers)
    magnitude = np.abs(stft_matrix)  # Shape: (n_fft/2+1, time_frames)
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)  # Frequency bins

    # Define Frequency Bands (Example)
    bands = {
        "Sub-Bass": (20, 60),
        "Bass": (60, 150),
        "Low-Midrange": (150, 400),
        "Midrange": (400, 1000),
        "Upper-Midrange": (1000, 2500),
        "Presence": (2500, 5000),
        "Brilliance Low": (5000, 10000),
        "Brilliance High": (10000, 20000),
    }

    # Find indices for each frequency band
    band_indices = {
        band: np.where((frequencies >= low) & (frequencies <= high))[0]
        for band, (low, high) in bands.items()
    }

    # Sum the energy in each band across time
    band_signals_over_time = {}
    for band, indices in band_indices.items():
        # Sum magnitudes for the current band across the indices
        energy = magnitude[indices, :].sum(axis=0)
        signals = [level >= 1 for level in energy]
        band_signals_over_time[band] = signals

    return band_signals_over_time

def writeBandSignalsToRegistery(band_signals_over_time):

    bandKeys = list(band_signals_over_time.keys())

    for i in range(len(band_signals_over_time[bandKeys[0]])):

        register = [False] * 8
        for j, band in enumerate(bandKeys):
            register[j] = band_signals_over_time[band][i]

        output(register)
        time.sleep(.1)






try:

    setup()
    y, sr = loadAudio()
    band_signals_over_time = dsp(y, sr)
    writeBandSignalsToRegistery(band_signals_over_time)


except KeyboardInterrupt:
    pass

finally:
    teardown()
    pass
