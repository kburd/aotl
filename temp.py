import librosa
import numpy as np
import matplotlib.pyplot as plt

# Plot the energy over time for each band
plt.figure(figsize=(10, 6))
for band, energy in band_signals_over_time.items():
    plt.plot(energy, label=band)
plt.title("Frequency Band Energies Over Time")
plt.xlabel("Time Frames")
plt.ylabel("Energy")
plt.legend()
plt.tight_layout()
plt.show()

