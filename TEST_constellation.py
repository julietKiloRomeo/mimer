# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 09:40:19 2014

@author: dk122
"""

from constellation import analyze_bite
import pylab as plt
from scipy.io import wavfile

fname1    = 'sound/seinfeld_percentage.wav' 
fname2    = 'sound/south_park_ask_mr_hat.wav'

fs, data    = wavfile.read(fname1)
P1, IM1 = analyze_bite(0, len(data), data, fs)

fs, data    = wavfile.read(fname2)
P2, IM2 = analyze_bite(0, len(data), data, fs)





plt.close('all')


f, axarr = plt.subplots(1,2, sharey=True)

axarr[0].imshow(IM1, aspect="auto", cmap='jet')
for (x,y) in zip(P1[0],P1[1]):
    axarr[0].plot(y,x,'o', color=(1,0.1,0.1,0.4), markersize=12)
axarr[0].set_title(fname1)



axarr[1].imshow(IM2, aspect="auto", cmap='jet')
for (x,y) in zip(P2[0],P2[1]):
    axarr[1].plot(y,x,'o', color=(1,0.1,0.1,0.4), markersize=12)
axarr[1].set_title(fname2)

plt.show()








