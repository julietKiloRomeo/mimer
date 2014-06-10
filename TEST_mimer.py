# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 09:58:37 2014

@author: dk122
"""

from mimer_lib import mimer
from scipy.io import wavfile
import os

os.system('cls')


def score(x):
    return x[3]*1.0/x[1]


testfile    = 'sound/seinfeld_percentage.wav' 
testfile    = 'sound/seinfeld_doubledip.wav'
testfile    = 'sound/south_park_ask_mr_hat.wav'
testfile    = 'sound/batman_ordinary.wav'

fs, data    = wavfile.read(testfile)

M           = mimer(fs)

for T in range(8):
    idx         = (T+0.2)*1.0*fs
    bite        = data[idx:idx + 2.0*fs]
    out         = M.process(bite)
    
    print "\n%-40s  %10s     %4s" % ('Name', 'Match', 'Time')
    for o in out:
        print "%-40s  %10.0f     %4.1f" % (o[0], score(o) , o[2])
    

import pylab as plt

plt.close('all')
NN = 1
fig, axarr = plt.subplots(1,2, figsize=(20,18))
axarr[0].plot(out[NN][4][0] ,out[NN][4][1],'o', color=(1,0.1,0.1,0.4), markersize=12)   

dT      = [t1-t2 for (t1,t2) in zip(out[NN][4][0], out[NN][4][1])]

axarr[1].hist(dT)



