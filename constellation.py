# -*- coding: utf-8 -*-
"""
Created on Wed May 28 11:30:26 2014

@author: dk122
"""
import Wavelets
import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import binary_erosion


def detect_peaks(image):
    """
    Takes an image and detect the peaks usingthe local maximum filter.
    Returns a boolean mask of the peaks (i.e. 1 when
    the pixel's value is the neighborhood maximum, 0 otherwise)
    """
    N = 51
    neighborhood = np.ones((N,N))==1
    #apply the local maximum filter; all pixel of maximal value 
    #in their neighborhood are set to 1
    local_max = maximum_filter(image, footprint=neighborhood)==image
    #local_max is a mask that contains the peaks we are 
    #looking for, but also the background.
    #In order to isolate the peaks we must remove the background from the mask.

    #we create the mask of the background
    background = (image==0)

    #a little technicality: we must erode the background in order to 
    #successfully subtract it from local_max, otherwise a line will 
    #appear along the background border (artifact of the local maximum filter)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    #we obtain the final mask, containing only peaks, 
    #by removing the background from the local_max mask
    detected_peaks = local_max - eroded_background

    return detected_peaks



def constellation(data, fs):

    wavelet = Wavelets.MorletReal(data, largestscale=16, notes=0, order=8, scaling="log")
    cwtmatr = np.absolute(wavelet.cwt)
    
    peaks   = detect_peaks(cwtmatr)
    
    mu_cwt  = np.outer( np.ones(cwtmatr.shape[0]),   cwtmatr.mean(axis=0) )
    rho_cwt = np.std(cwtmatr)
    
    peaks   = peaks & (cwtmatr > (mu_cwt + rho_cwt*3))
    # return peaks as list of coordinates
    coord = np.where(peaks)
    return coord, cwtmatr
    
def analyze_bite(I_start, N, data, fs):
    soundbite = data[I_start:I_start+N]
    peaks, cwtmatr = constellation(soundbite, fs)
#    peaks[1] += I_start    
#    peaks[1][:] /= fs
    out = (peaks[0], (peaks[1]+I_start)*1.0/fs)
    return out, cwtmatr
