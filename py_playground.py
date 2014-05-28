# -*- coding: utf-8 -*-
"""
Created on Tue May 27 13:06:42 2014

@author: dk122
"""
import numpy as np
import pylab as plt
from scipy.io import wavfile
from constellation import constellation
import matplotlib.animation as animation



fs, data = wavfile.read('daisy16.wav')
T = np.arange(len(data))/fs

peaks, cwtmatr = constellation(data, fs)


fig, ax = plt.subplots(2, 1, sharex=True)
fig.set_size_inches(20,15, forward=True)


ax[0].plot(data)
ax[1].imshow(-cwtmatr, aspect="auto", cmap='gray')
#ax[1].spy(peaks, aspect="auto", marker='.')
ax[1].plot(peaks[1],peaks[0], '.' )



def analyze_bite(I_start, N):
    soundbite = data[I_start:I_start+N]
    peaks, cwtmatr = constellation(soundbite, fs)
    return peaks, cwtmatr

p, cwt = analyze_bite(0, 100)
sp, = ax[1].plot(p[1],p[0], marker='s',linestyle='None', color=(1,0,0,0.5))

#
#
#
def animate(II):
    p, cwt = analyze_bite(II, 5000)
    sp.set_xdata(p[1]+II)
    sp.set_ydata(p[0])
    return sp,
#
#
ani = animation.FuncAnimation(fig, animate, np.arange(0,120000,1000), 
    interval=100)
plt.show()





