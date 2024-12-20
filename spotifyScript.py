import pyaudio
import numpy as np

# Set up parameters for audio sampling
FORMAT = pyaudio.paInt16  # Format for audio
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (44.1kHz)
CHUNK = 1024  # Number of frames per buffer

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

print("Recording...")

while True:
    # Read data from audio stream
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)

    # Process the audio signal
    rms = np.sqrt(np.mean(data**2))  # Calculate Root Mean Square (RMS) of the signal
    
    # Set a threshold for RMS to trigger GPIO pin (adjust based on your needs)
    if rms > 500:
        print("Audio above threshold, activating GPIO pin")
        # Activate GPIO pin based on audio volume
        # You can trigger GPIO actions here

    # You can also process frequencies, peaks, etc., for more advanced control
