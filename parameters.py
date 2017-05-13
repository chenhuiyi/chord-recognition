## specify the following parameters

## load file
# directory
dir = "audiosamples"
# filename
filename = "PianoChordsElectric.wav"
file = dir + "/" + filename
# offset: starting reading after this time (in seconds)
offset = 0
# duration: only load up to this much audio (in seconds)
duration = 50

## chromagram
# sr: sampling rate
sr = 44100
# hop_length: number of samples between successive chroma frames (frame size)
hop_length = 4096

## chordgram
# w: filter size; w = 30 to be a good comromise that works well for most songs
w = 30