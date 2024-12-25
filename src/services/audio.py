
import pyaudio
from utils.config import config
from services.register import RegisterService

registerService = RegisterService()
def process(data, frame_count, time_info, status):

    # Process Audio
    audio_signal = np.frombuffer(data, dtype=np.int16)
    fft_result = np.fft.fft(audio_signal)                    
    magnitude = np.abs(fft_result[:config.chunk_size // 2])

    # Calculate bands
    freqs = np.fft.fftfreq(frame_count, 1 / config.sample_rate)
    positive_freqs = freqs[:frame_count // 2] 

    binary_number = 0
    
    for i, (band_name, (low_freq, high_freq)) in enumerate(config.bands.items()):
        band_indices = np.where((positive_freqs >= low_freq) & (positive_freqs <= high_freq))[0]            
        band_magnitude_sum = np.sum(magnitude[band_indices])
        if band_magnitude_sum > config.threshold:
            binary_number |= (1 << i)

    # Output to Register
    registerService.write(binary_number)

    return (data, pyaudio.paContinue)


class AudioService:

    def __init__(self):
        self.registerService = 
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start(self):

        # Find the loopback device
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            print(device_info)
        
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=config.sample_rate,
            frames_per_buffer=config.chunk_size,
            input=True,
            input_device_index=3,
            output=True,
            output_device_index=0,
            stream_callback=process
        )

        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.registerService.shutdown()