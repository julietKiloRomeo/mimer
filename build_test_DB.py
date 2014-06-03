# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 13:18:31 2014

@author: dk122
"""

#import numpy as np
import pylab as plt
from scipy.io import wavfile
from constellation import analyze_bite
from episode_table import episode_table


ET = episode_table('test_DB.pkl')

fname       = 'daisy16.wav'
is_in_DB    = fname in ET.names
fs, data    = wavfile.read(fname)

if not is_in_DB:
    
    for i_start in range(0,len(data),1000):
        p, cwt = analyze_bite(i_start, 5000, data, fs)
        ET.add_map(p[0], p[1], fname)

fname       = 'sorry16.wav'
is_in_DB    = fname in ET.names

if not is_in_DB:
    fs, data    = wavfile.read(fname)
    
    for i_start in range(0,len(data),1000):
        p, cwt = analyze_bite(i_start, 5000, data, fs)
        ET.add_map(p[0], p[1], fname)

ET.save()


ep_matches = dict()

for i_start in range(0,10000,1000):
    p, cwt = analyze_bite(i_start, 5000, data, fs)
    
    for f,T_real in zip(p[0],p[1]):
        matches = ET.hashtable[f]
        for match in matches:
            T = match[0]
            ep = match[1]
            if not ep_matches.has_key(ep):
                ep_matches[ep] = [[],[]]
            ep_matches[ep][0].append(T_real)
            ep_matches[ep][1].append(T)







print 'plotting...'

print len(ep_matches['daisy16.wav'])

print ep_matches['daisy16.wav'][1][0:10]

plt.cla()
plt.plot(ep_matches['daisy16.wav'][0][0:1000],ep_matches['daisy16.wav'][1][0:1000], 'ro')
plt.show()

#for (x, y) in ep_matches['daisy16.wav']:
#    plt.plot(x, y, 'r+')
#for (x, y) in ep_matches['sorry16.wav']:
#    plt.plot(x, y, 'bo')
#    
#plt.show()
        


