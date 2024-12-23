import pyaudio, time

p = pyaudio.PyAudio()

chunk_size = 1024
sample_rate = 44100 

# Find the loopback device
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    print(device_info)

# Define callback for playback (1)
def callback(data, frame_count, time_info, status):
    # audio_signal = np.frombuffer(data, dtype=np.int16)
    # fft_result = np.fft.fft(audio_signal)                    
    # magnitude = np.abs(fft_result[:chunk_size // 2])
    # binary_number = calculate_band_sums(magnitude, chunk_size, 10_000_000)
    # writeToRegister(binary_number)
    print(data)
    return (data, pyaudio.paContinue)

# Open the default input stream
input_stream = p.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=sample_rate,
                      input=True,
                      input_device_index=3,
                      frames_per_buffer=chunk_size)

# Open the default output stream
output_stream = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=sample_rate,
                       output=True,
                       frames_per_buffer=chunk_size)

# Read and write audio data in chunks
while True:
    data = input_stream.read(1024)
    output_stream.write(data)

# Close the streams and terminate PyAudio
input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()


# # Wait for stream to finish (4)
# while stream.is_active():
#     time.sleep(0.1)

# # Close the stream
# stream.stop_stream()
# stream.close()
# p.terminate()