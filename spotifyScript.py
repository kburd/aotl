import alsaaudio
import numpy as np

# Open ALSA PCM device for capture
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
inp.setchannels(2)  # Set to stereo (1 for mono, 2 for stereo)
inp.setrate(44100)  # Set sample rate (same as Raspotify)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)  # 16-bit sample size
inp.setperiodsize(1024)  # Number of frames per buffer

while True:
    l, data = inp.read()
    if l:
        audio_data = np.frombuffer(data, dtype=np.int16)
        print(np.max(np.abs(audio_data)))  # Print maximum amplitude
