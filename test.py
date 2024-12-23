import pyaudio, time
import numpy as np

# ============== DEFAULT VALUES ==============

chunk_size = 1024
sample_rate = 44100 
gpio_pins = [2, 3, 4, 17, 27, 22, 10, 9] 

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

# ============== UTILITY FUNCTIONS ==============

def calculate_band_sums(magnitude, frame_count, threshold):

    freqs = np.fft.fftfreq(frame_count, 1 / sample_rate)
    positive_freqs = freqs[:frame_count // 2]    

    binary_number = 0
    
    for i, (band_name, (low_freq, high_freq)) in enumerate(bands.items()):
        # Find indices corresponding to the frequency band
        band_indices = np.where((positive_freqs >= low_freq) & (positive_freqs <= high_freq))[0]
        
        # Sum the magnitudes in this frequency band
        band_magnitude_sum = np.sum(magnitude[band_indices])
        
        if band_magnitude_sum > threshold:
            binary_number |= (1 << i)  # Set the i-th bit to 1
    
    return binary_number

def writeToRegister(value):

    for i, pin in enumerate(gpio_pins):
        bit = (value >> i) & 1
        GPIO.output(pin, bit)

def setupGPIO():

    GPIO.setmode(GPIO.BCM)

    for pin in gpio_pins:
        GPIO.setup(pin, GPIO.OUT)

def shutdownGPIO():
    GPIO.cleanup()

# ============== MAIN ==============

setupGPIO()
p = pyaudio.PyAudio()

# Find the loopback device
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    print(device_info)


# Open the default output stream
output_stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=sample_rate,
    frames_per_buffer=chunk_size,
    output=True
)

# Define callback for playback (1)
def callback(data, frame_count, time_info, status):
    audio_signal = np.frombuffer(data, dtype=np.int16)
    fft_result = np.fft.fft(audio_signal)                    
    magnitude = np.abs(fft_result[:chunk_size // 2])
    binary_number = calculate_band_sums(magnitude, chunk_size, 10_000_000)
    writeToRegister(binary_number)
    output_stream.write(data)
    return (data, pyaudio.paContinue)

# Open the default input stream
input_stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=sample_rate,
    frames_per_buffer=chunk_size,
    input=True,
    input_device_index=2,
    stream_callback=callback
)

# Wait for stream to finish (4)
while stream.is_active():
    time.sleep(0.1)

# Close the streams and terminate PyAudio
input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()
shutdownGPIO()