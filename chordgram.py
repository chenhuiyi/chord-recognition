from parameters import *
from chromagram import *
import librosa
import librosa.display
import numpy as np
from scipy.stats import mode

def generate_template():
    template = {}
    majors = ["C","Db","D","Eb","E","F","F#","G","Ab","A","Bb","B"]
    minors = ["Cm","Dbm","Dm","Ebm","Em","Fm","F#m","Gm","Abm","Am","Bbm","Bm"]

    # template for C and Cm
    tc = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
    tcm = [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
    shifted = 0

    for chord in majors:
        template[chord] = tc[12 - shifted:] + tc[:12 - shifted]
        shifted += 1

    for chord in minors:
        template[chord] = tcm[12 - shifted:] + tcm[:12 - shifted]
        shifted += 1

    # template for no chords
    tnc = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    template["NC"] = tnc

    return template

def cossim(u, v):
    """
    :param u: non-negative vector u
    :param v: non-negative vector v
    :return: the cosine similarity between u and v
    """
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def chordgram(C, display=False):
    """
    :param C: chromagram C
    :return: chordgram H
    """
    frames = C.shape[1]

    # initialize
    template = generate_template()
    chords = list(template.keys())
    chroma_vectors = np.transpose(C)
    # chordgram
    H = []

    for n in np.arange(frames):
        cr = chroma_vectors[n]
        sims = []

        for chord in chords:
            t = template[chord]
            # calculate cos sim, add weight
            if chord == "NC":
                sim = cossim(cr, t) * 0.7
            else:
                sim = cossim(cr, t)
            sims += [sim]
        H += [sims]
    H = np.transpose(H)

    if display == True:
        plt.figure(figsize=(10, 5))
        librosa.display.specshow(H, sr=sr, x_axis="frames")
        plt.title("Chordgram")
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    return H

def smoothing(s):
    """
    :param s: sequence s
    :return: mode filter for sequence s
    """
    w = 15
    news = [0] * len(s)
    for k in np.arange(w, len(s) - w):
        m = mode([s[i] for i in range(k - w // 2, k + w // 2 + 1)])[0][0]
        news[k] = m
    return news

def smoothed_chordgram(H, display=False):
    """
    :param H: chordgram
    :return: chordgram after filtering
    """
    chords = H.shape[0]
    H1 = []

    for n in np.arange(chords):
        H1 += [smoothing(H[n])]

    H1 = np.array(H1)
    if display == True:
        plt.figure(figsize=(10, 5))
        librosa.display.specshow(H1, sr=sr, x_axis="frames")
        plt.title("Chordgram")
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    return H1

def chord_sequence(H):
    """
    :param H: chordgram H
    :return: a sequence of chords
    """
    template = generate_template()
    chords = list(template.keys())

    frames = H.shape[1]
    H = np.transpose(H)
    R = []

    for n in np.arange(frames):
        index = np.argmax(H[n])
        if H[n][index] == 0.0:
            chord = "NC"
        else:
            chord = chords[index]

        R += [chord]

    return R

def tostring_chords(input):
    string = ""
    for r in input:
        if r == "NC":
            string += " -"
        else:
            string += " " + r
    return string

# Chord-Recognition Done!
C = chromagram(file)
H = chordgram(C)
H1 = smoothed_chordgram(H)
R = chord_sequence(H)
R1 = chord_sequence(H1)

print("[CHORD-RECOGNITION]")
print("File:", file)
print("Time:", offset, "to", offset + duration)
print("[Chords w/t smoothing]")
print(tostring_chords(R))
print("[Chords w/ smoothing]")
print(tostring_chords(R1))