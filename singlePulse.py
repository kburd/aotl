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

    try:

        setupGPIO()
        
        with True:

            writeToRegister(1)
            time.sleep(1)

            writeToRegister(1)
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        
        shutdownGPIO()
