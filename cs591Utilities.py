"""
 File: cs591Utilities.py
 Author: Wayne Snyder

 Date: 1/28/17
 Purpose: This collects together the most important algorithms used in
          CS 591, in order to work interactively; for the most part
          signals are manipulated as arrays, not as wave files.
          This file assumes you have scipy and numpy.
          
          The main difference from previous version is that
          we are using numpy arrays exclusively. 
"""

import array
import contextlib
import wave
import numpy as np
import matplotlib.pyplot as plt
#from numpy import pi, sin, cos, exp, abs
#from scipy.io.wavfile import read, write


"""
 Basic parameters
"""


numChannels   = 1                      # mono
sampleWidth   = 2                      # in bytes, a 16-bit short
SR            = 44100                  #  sample rate
MAX_AMP       = (2**(8*sampleWidth - 1) - 1)    #maximum amplitude is 2**15 - 1  = 32767
MIN_AMP       = -(2**(8*sampleWidth - 1))       #min amp is -2**15

"""
 File I/O        
"""

# Read a wave file and return the entire file as a standard array
# infile = filename of input Wave file
# If you set withParams to True, it will return the parameters of the input file

def readWaveFile(infile,withParams=False,asNumpy=True):
    with contextlib.closing(wave.open(infile)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
        if(params[0] != 1):
            print("Warning in reading file: must be a mono file!")
        if(params[1] != 2):
            print("Warning in reading file: must be 16-bit sample type!")
        if(params[2] != 44100):
            print("Warning in reading file: must be 44100 sample rate!")
    if asNumpy:
        X = array.array('h', frames)
        X = np.array(X,dtype='int16')
    else:  
        X = array.array('h', frames)
    if withParams:
        return X,params
    else:
        return X