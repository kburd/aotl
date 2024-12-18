import wave, sys, pyaudio
import numpy as np
import RPi.GPIO as GPIO


def setupGPIO():

    GPIO.setmode(GPIO.BCM)

    for pin in gpio_pins:
        GPIO.setup(pin, GPIO.OUT)

def shutdownGPIO():
    GPIO.cleanup()

def calculate_band_sums(magnitude, positive_freqs, threshold):
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

# Define frequency bands
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


chunk_size = 1024
sample_rate = 44100  # Sample rate of the audio

gpio_pins = [2, 3, 4, 17, 27, 22, 10, 9] 

freqs = np.fft.fftfreq(chunk_size, 1 / sample_rate)
positive_freqs = freqs[:chunk_size // 2]  # Only positive frequencies

def callback(in_data, frame_count, time_info, status):

    data = wf.readframes(frame_count)
    audio_signal = np.frombuffer(data, dtype=np.int16)

    # Apply FFT to the chunk_size of audio data
    fft_result = np.fft.fft(audio_signal)
    
    # Get the magnitude of the frequencies (only positive frequencies)
    magnitude = np.abs(fft_result[:chunk_size // 2])

    binary_number = calculate_band_sums(magnitude, positive_freqs, 10_000_000)
    writeToRegister(binary_number)

    return (data, pyaudio.paContinue)

if len(sys.argv) < 2:
    print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

try: 
    
    setupGPIO()

    with wave.open(sys.argv[1], 'rb') as wf:
        # Instantiate PyAudio and initialize PortAudio system resources (1)
        p = pyaudio.PyAudio()

        # Open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)

        # Wait for stream to finish (4)
        while stream.is_active():
            time.sleep(0.1)


except KeyboardInterrupt:
    pass

finally:

    # Close the stream (5)
    stream.close()

    # Release PortAudio system resources (6)
    p.terminate()

    shutdownGPIO()