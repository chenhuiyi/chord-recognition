# chord-recognition
Team: [Lingyi(Echo) Gu](http://github.com/lingyigu), Huiyi Chen

## Getting Started
This project is developed using [Anaconda](https://docs.continuum.io/anaconda/install) with [Python3.3+](https://www.python.org/download/releases/3.0/). To install the Anaconda distribution, check the documentations [here](https://docs.continuum.io/anaconda/install).

This project has also used an external library [librosa](https://github.com/librosa/librosa).<br>
To install  ```librosa```:

    pip3 install librosa

To install ```librosa``` for Anaconda:

    conda install -c conda-forge librosa

To run the scripts, execute ```chordgram.py``` under the ```chord-recognition``` directory.
You can also modify the parameters in ```main.py``` as follows.

```python3
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
```

## Motivation
We're interested in developing a **Chord Recognition** tool that recognizes majors and minors.
When we're young, we both had experience with piano.
Recently Huiyi decides to pick up her piano skills, and Echo has been learning guitar for a while.
Sometimes when a song is relatively new, it's very unlikely to find a music sheet for it online.
If that's the case, I would go to websites like [Chordify](https://chordify.net/) and get the chords from there.
I'm definitely curious about how chord recognition works in general, so we decide to work on this topic.


## Algorithms
![algorithm](https://github.com/lingyigu/chord-recognition/blob/master/visualizations/algorithm.png)

#### Chromagram Calculation
The Chromagram could be constructed as spectrograms, which represents the relationship between time and frequency spectrum.
The frequency spectrum is formed by 12-dimensional chroma vectors, which is a set of pitch classes ```{C, Db, D, Eb, E, F, F#, G, Ab, A, Bb, B}```, and each element of the vector shows the strength of the input.
The computation of the Chromagram is to calculate the frequency and amplitudes of the corresponding note from the spectrogram.

There are many ways to calculate it as discussed in different papers.
Short-time Fourier Transform, Constant Q Transform and Fast Fourier Transform are the three common ones that people use.
We have implemented two of them during the progress of this project, the CQT approach and the FFT approach.
The CQT approach is the method that we have chosen for template matching later. Partial code for FFT has also been attached by the end of ```chromagram.py``` file.

A good way to visualize the Chromagram is a two-dimensional image, showing time or number of frames on the x axis and 12 pitch classes on the y axis.
We can easily identify which pitches being the strongest according to the color.

Given the audio ```PianoChordsElectric.wav``` provided under the ```audiosamples``` directory, here's the Chromagram produced by analyzing the wave file between 0:00 - 0:50.
For the rest of our analysis, we always uses this segment of the wave file.

![set1](https://github.com/lingyigu/chord-recognition/blob/master/visualizations/set1.png)

Here's another chromagram produced by analyzing the same wave file between 0:55 - 1:45.

![set2](https://github.com/lingyigu/chord-recognition/blob/master/visualizations/set2.png)

#### Chordgram Calculation
The next thing we need to do is to determine the chord probabilities from the chroma vectors we have calculated from the previous step.
It is basically a comparison between the typical distributions of chords and the energy computed in the chroma vectors to estimate the correct chord.
We will do this analysis frame by frame.

###### Template
The set of chords we want to detect is the 12 major chords, 12 minor chords and a "N.C" chord, which stands for "no chord".
Given the template for ```C``` and ```Cm``` as follows, we can generate the templates for all 24 chords simply by shifting the numbers in the array.

    C major = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
    C minor = [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]

For the special chord, the "no chord", all pitch classes are weighted equally. The template for "N.C" is given as [Christoph Hausner].

    N.C. = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

###### Cosine Similarity
Then we can match the chroma vector calculated for the current frame against the template.
It is trivial to use the Euclidean Distance as many researchers do, however, we decide to adopt the [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) computation.
Since we want to improve the ability of our algorithm to detect complex chords, we find this method gives us a slightly more accurate result thant the Euclidean Distance can offer.
By computing the cosine similarity between chroma vectors and the template for each frame, we obtain the Chordgram as a result. 

Here's the Chordgram produced.
![chordgram](https://github.com/lingyigu/chord-recognition/blob/master/visualizations/chordgram.png)

#### Chord Sequence Estimation
We can also estimate the chord sequences from the Chordgram obtained.
In order to do this, we compute the chord with the highest probability during each time step. 

###### Mode Filter
Before that, there's another factor we need to take into consideration: noises.
One way we can solve this is to apply a mode filter presented by [Christoph Hausner], which filters by computing the mode of all values in a neighborhood and ```w``` stands for the filter size.
In our cases, we have set ```w = 15``` after testing a few different values. We find this value works fine in this scenario.
Sometimes we need a larger filter size since it will make the smoothing stronger if twe only have slow-changing chords, generally w = 30 is adequate. 
We may also repeat the smoothing process to obtain a more accurate results.

    R[r] = mode { R[r - w / 2], ..., R[r + w / 2]}

Here's the Chordgram produced after smoothing.
![chordgram-smoothed](https://github.com/lingyigu/chord-recognition/blob/master/visualizations/chordgram-smoothed.png)

###### Results
According to the smoothed Chordgram, we obtain the most likely chord for each frame using cosine similarity.
Here's the output. It's easy to see that the chords estimated without using a smoothing filter has more fluctuations.

    [CHORD-RECOGNITION]
    File: audiosamples/PianoChordsElectric.wav
    Time: 0 to 50
    [Chords w/t smoothing]
     Bb - - Bb - - Bb - B - - - - Eb - Eb - - F# - D - - - Eb Eb - - - - Eb Eb Eb - - - Ab Ab C C C C Ab C Ab C Ab C C C C C C C C C C Em Em Em Em Em Em Em Em E - - - C - - - - - - - - - - - - - - - - - E - G G G G G G G G G G G G G G G G G G G G G G G G G G G G G G - - - - G - - - - F# Eb - - Bb Bb - - Eb D D D D D D D D D D D D D D D D D D D D D D D D D Bb D D D - - - - Eb E B - - F - - - - - - - - - - A A A A A A A A A A A A A A A A A A A A A A A A A A A A A A A - - - - - - - B - - - D E A A A A A A A A A A A A A A A A A A A A A A A A Ab Ab Ab A A Ab A - - - - - - F B B B B B B B B B G G G G G G G G G G G G B B C C C C Eb - - - Eb - - C - - - B - - F# F# F# F# F# F# F# F# F# F# F# F# F# F# F# F# F# F# F# F# F# F# B G B F# - - - B Eb - - - - - G - A A A A A A A A A A A A A A Fm Fm A Fm Fm Fm Fm Fm Fm Fm Fm Fm Fm Fm Fm A A A - - F# - - - Db - - - Bb Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab Ab A A Ab A Ab - - - - - - Bb D - - Ab Ab Ab Ab G Ab Ab Ab Ab Ab Ab Ab G G G G G G G G Gm G Ab - G - Eb - Eb Eb - Eb Eb Eb - - F# - A Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb F# F# F# F# F# G - - - Eb Eb - B - Db F F F F F F F F F F F F F F F F F F F F F F F F F F F F F F F F F Bb F F
    [Chords w/ smoothing]
     - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - G G G G G G G G G G C G C Ab C C C C C C Em Em Em Em Em Em Em Em Em Em C C C C - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Eb G G G G G G G G G G G G G G G G G G G G G G G G G Eb - - - - - - - - - - - - - - - - - - - - - - D D D D D D D D D D D D D D D D Bb D D Bb - - - - - - - - - - - - - - - - - - - - - - - - - - - - - F A A A A A A A A A A A A A A A A A A A Bb Bb Bb Bb Bb - - - - - - - - E E E E E E E E Db Ab Ab Ab A A A A A A A A A A A A A A A A A E E E E E E E E - - - - - - - - - - - F# F# G G G G G G G G B B B B B Bm G B B B B B B B B B B - - - - - - - - - - - - - - F# F# F# F# F# F# F# F# F# F# F# B B F# F# F# F# F# B B B B B - - - - - - - - - - - - - - Ab Ab Ab A A A A A A A Fm Fm Fm Fm Fm Fm Fm Fm Fm A A A A Db - - - - - - - - - - - Db Db Db Db Db Db Db Db Db Db Db Ab Ab Ab Ab Ab Ab Ab Ab Ab A A A A A A Ab Ab Ab Ab Ab Db Db Db Db - - - Eb Eb G G G G Eb Eb Eb Eb G Ab G G G G G G G G Gm Gm Eb Eb Eb Eb Eb Eb Eb Eb Eb Eb - - - - - - - - - - Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb Bb F# F# F# F# F# F# Bb Bb Bb Bb Bb Bb Bb - - - - - - - - - - - - - Db F F F F F F F F F F F F F F F - - - - - - - - - - - - - - -

We can also compare it to the actual chord information as in ```PinaoChordsDescription.txt```.
As we can see, the general chord information is correct. Although it doesn't do a good job with ```C``` and ```Ab```.

    Set 1 (0:0 - 0:50): The 12 major chords in root position (i.e., C major would be C-E-G)
     played in the circle of fifths:
            C, G, D, A, E, B, F#, C#, Ab, Eb, Bb, F

## Limitations and Future Work
1. This program would only works well for an audio file of pure piano chords, like the ones provided in the ```audiosample``` directory.
(I have tried it with a pop song, terrible result!)

2 .In this program, we have chosen to use a simple filter method. Again, this strategy doesn't clean up the noises as much as we want.
We may need to combine different filters, such as the low-pass and median-pass filters together.

2. A few chords are off. We may improve this by trying different measures of fit and find a better one for this particular kind of music file.

3. It does not have an user interface yet.
Web would be a pretty good way to present this tool since users can just go on the website and check the chords of a song.

## Reference
1. **"Spectral Analysis"**.[http://www.cs.bu.edu/snyder/cs591/Lectures/SpectralAnalysisChords.pdf](http://www.cs.bu.edu/~snyder/cs591/Lectures/SpectralAnalysisChords.pdf).

2. **"CHORD RECOGNITION USING MEASURES OF FIT, CHORD TEMPLATES AND FILTERING METHODS"**, by Laurent Oudre, Yves Grenier, and Cédric Févotte: [http://www.ee.columbia.edu/dpwe/papers/OudGF09-chords.pdf](http://www.ee.columbia.edu/~dpwe/papers/OudGF09-chords.pdf).

3. **"TEMPLATE-BASED CHORD RECOGNITION : INFLUENCE OF THE CHORD TYPES"** by Laurent Oudre, Yves Grenier, and Cédric Févotte: [http://laurentoudre.fr/publis/OGF-ISMIR-09.pdf](http://laurentoudre.fr/publis/OGF-ISMIR-09.pdf).

4. **"Design and Evaluation of a Simple Chord Detection Algorithm"** by Christoph Hausner: [http://www.fim.uni-passau.de/fileadmin/files/lehrstuhl/sauer/geyer/BA_MA_Arbeiten/BA-HausnerChristoph-201409.pdf](http://www.fim.uni-passau.de/fileadmin/files/lehrstuhl/sauer/geyer/BA_MA_Arbeiten/BA-HausnerChristoph-201409.pdf)