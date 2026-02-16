import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(duration, fs, samplerate=44100):
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    write("../audio.wav", samplerate, audio_data)
    print("Recording finished")


record_audio(5, 44100)