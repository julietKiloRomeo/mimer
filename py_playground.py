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
import pywt


def nextpow2(i):
    n = 2
    while n < i: n = n * 2
    return n
    



tmp = np.zeros(nextpow2(len(data)))
tmp[:len(data)] = data
data = tmp

print len(data)

w_coeff = (data,)
T       = (np.arange(len(data)),)
IM      = np.array([])
cA      = data

X       = []
Y       = []
Z       = []

for i in range(8):
    cA, cD  = pywt.dwt(cA, 'db2')
    w_coeff = w_coeff + (cD,)
    T       = T + (np.arange(len(cD))*2**(i+1),)
    imline = np.array([np.kron(cD, np.ones((2**(i+1))))])
    
    dx = np.linspace(0,1,len(cA))    
    dy = np.zeros(len(cA)) + i   
    dz = cA
    
    if len(cA) < 60000:    
        X = np.append(X, dx)
        Y = np.append(Y, dy)
        Z = np.append(Z, dz)
    
#    if len(IM)==0:
#        IM = imline
#    else:
#        IM = np.append(IM, imline, axis=0)
#    print np.size(imline)
#    
#print np.size(IM)


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#f, ax = plt.subplots(3, 1)
#
#ax[0].plot(T[0], np.abs(w_coeff[0]))
#for j in range(3):
#    ax[j].plot(T[j+8], np.abs(w_coeff[j+8]))
#

fig = plt.figure(figsize=(5,5) )
ax = fig.gca(projection='3d')


ax.plot_trisurf(X,Y,Z, cmap=cm.jet, linewidth=0.2, edgecolor=(0,0,0,0)  )
ax.view_init(elev=90., azim=0)
plt.show()















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