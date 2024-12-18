import wave, time, sys, pyaudio
import numpy as np
import RPi.GPIO as GPIO

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

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
        sys.exit(-1)

    try:

        setupGPIO()
        
        with wave.open(sys.argv[1], 'rb') as wf:

            # Define callback for playback (1)
            def callback(in_data, frame_count, time_info, status):
                data = wf.readframes(frame_count)
                audio_signal = np.frombuffer(data, dtype=np.int16)
                fft_result = np.fft.fft(audio_signal)                    
                magnitude = np.abs(fft_result[:frame_count // 2])
                binary_number = calculate_band_sums(magnitude, frame_count, 10_000_000)
                writeToRegister(binary_number)
                return (data, pyaudio.paContinue)

            # Instantiate PyAudio and initialize PortAudio system resources (2)
            p = pyaudio.PyAudio()

            # Open stream using callback (3)
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
