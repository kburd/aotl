import pyaudio

p = pyaudio.PyAudio()

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

# Find the loopback device
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if 'Loopback' in device_info['name']:
        loopback_index = i
        break

# Define callback for playback (1)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(chunk_size)
    # audio_signal = np.frombuffer(data, dtype=np.int16)
    # fft_result = np.fft.fft(audio_signal)                    
    # magnitude = np.abs(fft_result[:chunk_size // 2])
    # binary_number = calculate_band_sums(magnitude, chunk_size, 10_000_000)
    # writeToRegister(binary_number)
    print(data)
    return (data, pyaudio.paContinue)

# Open the loopback device for recording
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                input=True,
                input_device_index=loopback_index,
                stream_callback=callback)


# Wait for stream to finish (4)
while stream.is_active():
    time.sleep(0.1)

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()