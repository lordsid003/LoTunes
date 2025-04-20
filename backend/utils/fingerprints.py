import librosa
import io
import numpy as np
# Used to find the local maxima in the Spectrogram (for finding peak intensities)
from scipy.ndimage import maximum_filter

# Controls density of fingerprinting (each peak is paired with 15 neighbouring peaks)
FAN_VALUE: int = 15
# Minimum threshold amplitude to be considered as a peak (removes noise or irrelevant characteristics for compression)
MIN_AMPLITUDE: int = 10

def get_spectrogram(audio_data, sampling_rate: int = 44100, from_bytes: bool = False):
    if from_bytes:
        # Load audio directly from bytes
        audio_file, sample_rate = librosa.load(io.BytesIO(audio_data), sr=sampling_rate, mono=True)
    else:
        # Original behavior: load from file path
        audio_file, sample_rate = librosa.load(audio_data, sr=sampling_rate, mono=True)
    # Audio normalization for noise reduction and characteristic recognition
    audio_file = librosa.util.normalize(audio_file)
    # Short-time Fourier Transform (DFT) for converting Time-wavelength curve to Time-frequency curve 
    # The default value, n_fft=2048 samples, corresponds to a physical duration of 93 milliseconds at a sample rate of 22050 Hz
    # hop_length = number of audio samples between adjacent STFT columns
    spectrogram = np.abs(librosa.stft(audio_file, n_fft = 2048, hop_length = 512))
    return spectrogram, sample_rate

def get_peaks(spectrogram, amp_min: int = MIN_AMPLITUDE):
    # Neighbourhood size for sampling: 20 X 20
    # Reduces entire spectrogram to important landmarks
    struct = maximum_filter(spectrogram, size = (20, 20))
    peaks = (spectrogram == struct) & (spectrogram > amp_min)
    return np.argwhere(peaks) # returns [(freq_bin, time_bin), ...]

def get_remote_audio_fileName(song_name: str, artists: list[str]) -> str:
    return f"{song_name} - {artists[0]}.mp3"

def generate_hashes(peaks):
    hashes = []
    for i in range(len(peaks)):
        for j in range(1, FAN_VALUE):
            if i + j < len(peaks):
                f1, t1 = peaks[i]
                f2, t2 = peaks[i + j]
                delta_t = t2 - t1
                if 0 <= delta_t <= 200:
                    h = hash((f1, f2, delta_t))
                    hashes.append((int(h), int(t1)))
    return hashes