from parameters import *
import librosa
import librosa.display
import matplotlib.pyplot as plt

def chromagram(file, display=False):
    """
    :param file: file path
    :param sr: sample rate, default: 44100
    :return: chroma features of input audio
    instructions: https://librosa.github.io/librosa/generated/librosa.feature.chroma_cqt.html#librosa.feature.chroma_cqt
    
    """
    sr = 44100

    # reads audio file starting at [offset] and lasts [duration] seconds
    y, sr = librosa.load(file, sr=sr, offset=offset, duration=duration)

    # Harmonic content extraction
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # use Constant Q Transform to calculate Pitch Class Profile (PCP), normalized
    chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, hop_length=hop_length)

    if display == True:
        plt.figure(figsize=(10, 5))
        librosa.display.specshow(chromagram, sr=sr, x_axis="frames",  y_axis="chroma")
        plt.title("Chroma Features")
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    return chromagram

# class chromavector:
#     def __init__(self, x):
#         """
#         :param x: signal x or a frame of signal x
#         """
#         self.x = x
#         self.note = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
#         self.notes = {}
#         self.generate_freqs()
#
#     def generate_freqs(self):
#         """
#         :return: a dictionary of the frequencies for each key on the piano
#         """
#         semitone = 2 ** (1 / 12)
#         self.notes["A0"] = 27.5
#         self.notes["A#0"] = 27 * semitone
#         self.notes["B0"] = 27 * semitone * semitone
#         self.notes["C1"] = 27 * semitone * semitone * semitone
#         f = 27.5 * (2 ** (3 / 12))
#
#         for n in range(1, 8):
#             for note in self.note:
#                 self.notes[note + str(n)] = f
#                 f *= semitone
#
#     def FFT(self, w, n, sr, fmin, fmax, bins):
#         """
#         :param x: signal x
#         :param w: window size w
#         :param n: the current frame n
#         :param sr: the sample rate
#         :param fmin: lower frequency
#         :param fmax: upper frequency
#         :param bins: the number of bins in an octave
#         :return: calculate chroma vector for the current frame using FFT
#         """
#         # FFT
#         X = self.x
#         S = realFFT(X)
#         S = np.select([S > 0.001], [S])
#         F = np.array([i * sr / len(X) for i in range(len(S))])
#         # cut off higher frequencies
#         cut = int(5000 / sr * len(X))
#         S = S[:cut]
#         F = F[:cut]
#
#         # calculate spectrogram
#         incr = 2 ** (1 / 48)    # quad of semi-tone
#         spec = {}
#         notes = self.notes.keys()
#         for k in range(len(F)):
#             for note in notes:
#                 if (self.notes[note] / incr < F[k] and self.notes[note] * incr >= F[k]):
#                     if note in spec:
#                         spec[note] += np.log10(S[k])
#                     else:
#                         spec[note] = np.log10(S[k])
#                     break
#         # calculate chromagram
#         C = np.zeros(12)
#         for i in range(12):
#             for note in spec:
#                 if self.note[i] in note:
#                     C[i] += self.notes[note]
#
#         return C / (np.linalg.norm(C))