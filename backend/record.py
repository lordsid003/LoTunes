import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from utils.paths import get_recorded_path

def normalize_audio(audio):
    audio = audio.flatten()
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val  # Normalize to [-1.0, 1.0]
    return audio

def record_audio(filename: str, duration: int = 10, fs: int = 44100):
    # Recording frequency: 44100 Hertz
    print("🎙️ Recording for", duration, "seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()

    # Normalize
    normalized_audio = normalize_audio(audio)

    # Convert to int16 before saving
    audio_int16 = np.int16(normalized_audio * 32767)
    write(filename, fs, audio_int16)

    print("✅ Recording saved as", filename)

if __name__ == "__main__":
    fileName: str = str(input("File name for recording: "))
    RECORDED_PATH: str = get_recorded_path(fileName=fileName)
    record_audio(filename=RECORDED_PATH)