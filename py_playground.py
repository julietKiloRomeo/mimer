# -*- coding: utf-8 -*-
"""
Created on Tue May 27 13:06:42 2014

@author: dk122
"""
import numpy as np
import pylab as plt
from scipy.io import wavfile
from constellation import constellation, analyze_bite
import matplotlib.animation as animation



fs, data    = wavfile.read('daisy16.wav')
T           = np.arange(len(data))/fs

peaks, cwtmatr  = constellation(data, fs)
peaks           = ( np.array([]) , np.array([]) )

for i_norm in range(0,cwtmatr.shape[1]):
    s = sum(cwtmatr[:,i_norm])
    cwtmatr[:,i_norm] /= s



for i_start in range(0,120000,1000):
    p, cwt = analyze_bite(i_start, 5000, data, fs)
    peaks = (np.hstack([peaks[0], p[0]]), np.hstack([peaks[1], p[1]]))


fig, ax = plt.subplots(2, 1, sharex=True)
fig.set_size_inches(20,15, forward=True)


ax[0].plot(np.arange(cwtmatr.shape[1])*1.0/fs, data)
ax[1].imshow(-cwtmatr, aspect="auto", cmap='gray', extent=[0, cwtmatr.shape[1]/fs, 11, 0])
ax[1].plot(peaks[1],peaks[0], '.' )

p, cwt  = analyze_bite(0, 100, data, fs)
sp,     = ax[1].plot(p[1]*1.0/fs,p[0],  marker='s',
                                        linestyle='None', 
                                        color=(1,0,0,0.5))
#plt.xlim([0,120000])
#
#
def animate(II):
    p, cwt = analyze_bite(II, 5000, data, fs)
    sp.set_xdata(p[1]+II*1.0/fs)
    sp.set_ydata(p[0])
    return sp,
#
#
ani = animation.FuncAnimation(fig, animate, np.arange(0,110000,1000), 
    interval=10)
plt.show()





