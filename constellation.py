# -*- coding: utf-8 -*-
"""
Created on Wed May 28 11:30:26 2014

@author: dk122
"""

import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import binary_erosion
import scipy


def nextpow2(i):
    """
    Find 2^n that is equal to or greater than.
    """
    n = 1
    while n < i: n *= 2
    return n


def detect_peaks(image):
    """
    Takes an image and detect the peaks using the local maximum filter.
    Returns a boolean mask of the peaks (i.e. 1 when
    the pixel's value is the neighborhood maximum, 0 otherwise)
    """
    
    # size of neighborhood a peak has to be highest in
    N               = 11
    neighborhood    = np.ones((N,N))==1
    # apply the local maximum filter; all pixel of maximal value 
    # in their neighborhood are set to 1
    local_max = maximum_filter(image, footprint=neighborhood)==image
    # local_max is a mask that contains the peaks we are 
    # looking for, but also the background.
    # In order to isolate the peaks we must remove the background from the mask.

    # we create the mask of the background
    background = (image==0)

    # a little technicality: we must erode the background in order to 
    # successfully subtract it from local_max, otherwise a line will 
    # appear along the background border (artifact of the local maximum filter)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    # we obtain the final mask, containing only peaks, 
    # by removing the background from the local_max mask
    detected_peaks = local_max - eroded_background

    return detected_peaks
    

def stft(x, fs, framesz, stepsz):
    """
    Do short time fft in sequential winows of a signal
    
    Returns a 2D array with frequencies as function of time 
    where time is along the first dimension and frequency is along the second
    """
    
    # create window
    w = scipy.hamming(framesz)
    # do fft for each window
    X = scipy.array([scipy.fft(w*x[i:i+framesz]) for i in range(0, len(x)-framesz, stepsz)])
    # only take bottom half of symmetric fft
    N_half  = framesz//2+1
    X       = X[:,0:N_half]
    f       = np.linspace(0,fs/2,N_half);
    
    # return norm of fft and frequency vector
    return np.sqrt(X.real**2+X.imag**2), f

def constellation(data, fs):
    """
    Perform peak detection on an fft-energy-image and return the peaks as a list 
    of coordinates.
    
    Input is fft-norm and sampling frequency
    
    Returns a 2D array with frequencies as function of time 
    where time is along the first dimension and frequency is along the second
    """
    T_WIN       = 0.05
    WIN_SZ      = nextpow2(T_WIN*fs)
    STP_SZ      = WIN_SZ/4
    im,f        = stft(data, fs, WIN_SZ, STP_SZ)
    E           = np.inner(im, 1.0*np.diag(range(im.shape[1]))  )
    E           = E**2
    peaks       = detect_peaks(E)
    
    mu_E        = np.outer( np.ones(E.shape[0]),   E.mean(axis=0) )
    rho_E       = np.std(E)
    
    peaks       = peaks & (E > (mu_E + rho_E*5.0))
    # get list of coordinates
    coord       = np.where(peaks)
    # construct time vector
    T           = np.arange(0,E.shape[0])*1.0/fs*STP_SZ

    # return (T,f) coordinates
    TF_coord    = [[],[]]
    TF_coord[0] = T[coord[0]]
    TF_coord[1] = f[coord[1]]

    return TF_coord, E, (T,f)
    
def analyze_bite(T_start, dT, data, fs):
    
    I_start         = T_start*fs    
    N               = nextpow2(dT*fs)
    
    soundbite       = data[I_start:I_start+N]
    peaks, im, TF   = constellation(soundbite, fs)
    out             = (peaks[0], (peaks[1]))
    return out, im, TF























