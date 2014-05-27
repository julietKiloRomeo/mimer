# -*- coding: utf-8 -*-
"""
Created on Tue May 27 13:06:42 2014

@author: dk122
"""

import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion
import matplotlib.pyplot as pp

from scipy.io import wavfile

fs, data = wavfile.read('daisy16.wav')
print len(data)
import pywt



w_coeff = (data,)
T       = (np.arange(len(data)),)
IM      = np.array([])
cA      = data
for i in range(16):
    cA, cD  = pywt.dwt(cA, 'db2')
    w_coeff = w_coeff + (cD,)
    T       = T + (np.arange(len(cD))*2**(i+1),)
    imline = np.array([np.kron(cD[:-2], np.ones((2**(i+1))))])
    if len(IM)==0:
        IM = imline
#    else:
#        IM = np.append(IM, imline, axis=0)
#    print np.size(imline)
    
    


import matplotlib.pyplot as plt
#f, ax = plt.subplots(3, 1)
#
#ax[0].plot(T[0], np.abs(w_coeff[0]))
#for j in range(3):
#    ax[j].plot(T[j+8], np.abs(w_coeff[j+8]))
#


imgplot = plt.imshow(IM)

#plt.show()














#
##for some reason I had to reshape. Numpy ignored the shape header.
#paws_data = np.loadtxt("paws.txt").reshape(4,11,14)
#
##getting a list of images
#paws = [p.squeeze() for p in np.vsplit(paws_data,4)]
#
#
#def detect_peaks(image):
#    """
#    Takes an image and detect the peaks usingthe local maximum filter.
#    Returns a boolean mask of the peaks (i.e. 1 when
#    the pixel's value is the neighborhood maximum, 0 otherwise)
#    """
#
#    # define an 8-connected neighborhood
#    neighborhood = generate_binary_structure(2,2)
#
#    #apply the local maximum filter; all pixel of maximal value 
#    #in their neighborhood are set to 1
#    local_max = maximum_filter(image, footprint=neighborhood)==image
#    #local_max is a mask that contains the peaks we are 
#    #looking for, but also the background.
#    #In order to isolate the peaks we must remove the background from the mask.
#
#    #we create the mask of the background
#    background = (image==0)
#
#    #a little technicality: we must erode the background in order to 
#    #successfully subtract it form local_max, otherwise a line will 
#    #appear along the background border (artifact of the local maximum filter)
#    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
#
#    #we obtain the final mask, containing only peaks, 
#    #by removing the background from the local_max mask
#    detected_peaks = local_max - eroded_background
#
#    return detected_peaks
#
#
##applying the detection and plotting results
#for i, paw in enumerate(paws):
#    detected_peaks = detect_peaks(paw)
#    pp.subplot(4,2,(2*i+1))
#    pp.imshow(paw)
#    pp.subplot(4,2,(2*i+2) )
#    pp.imshow(detected_peaks)
#
#pp.show()