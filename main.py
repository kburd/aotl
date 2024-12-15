import librosa
import numpy as np
import matplotlib.pyplot as plt
# from music21 import stream, note

# Load the audio file
file_path = "./happy-birthday-266285.mp3"
y, sr = librosa.load(file_path)

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
band_energies_over_time = {}
for band, indices in band_indices.items():
    # Sum magnitudes for the current band across the indices
    energy = magnitude[indices, :].sum(axis=0)
    band_energies_over_time[band] = energy

# Plot the energy over time for each band
# plt.figure(figsize=(10, 6))
# for band, energy in band_energies_over_time.items():
#     plt.plot(energy, label=band)
# plt.title("Frequency Band Energies Over Time")
# plt.xlabel("Time Frames")
# plt.ylabel("Energy")
# plt.legend()
# plt.tight_layout()
# plt.show()

print(band_energies_over_time)