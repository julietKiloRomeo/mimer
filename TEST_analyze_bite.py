# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 11:41:28 2014

@author: dk122
"""
import os
os.system('cls')

from scipy.io import wavfile
from constellation import analyze_bite
import pylab as plt

fname       = 'sound/seinfeld_percentage.wav' 

fs, data    = wavfile.read(fname)


P, IM, TF   = analyze_bite(0, len(data)*1.0/fs, data, fs)

T_max = TF[0][-1]
f_max = TF[1][-1]



plt.close('all')

f, axarr    = plt.subplots(1,figsize = (20,18))


axarr.imshow(IM, aspect="auto", cmap='jet', extent=[0, f_max, T_max , 0] )

for i_start in range(0, len(data)-4096, 256):
    T_start = i_start*1.0/fs
    p, cwt, tf = analyze_bite(T_start, 1, data, fs)
    
    T_vect = p[0] + T_start
    f_vect = p[1]
    for (x,y) in zip(f_vect, T_vect):
        axarr.plot(x, y,'<', color=(0.1,1,0.1,0.4), markersize=8)


for (x,y) in zip(P[1],P[0]):
    axarr.plot(x,y,'o', color=(1,0.1,0.1,0.4), markersize=12)

print 'done'
#plt.show()
#


