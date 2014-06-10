# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 13:18:31 2014

@author: dk122
"""

#import numpy as np

from scipy.io import wavfile
from constellation import analyze_bite
from episode_table import episode_table

ET = episode_table('test_DB.pkl', 'clear')

episodes = ['batman_ordinary',
            'seinfeld_percentage',
            'seinfeld_doubledip',
            'south_park_ask_mr_hat']

def add_file(fname):

    is_in_DB    = fname in ET.names
    fs, data    = wavfile.read(fname)
    
    if not is_in_DB:
        p,cwt,FT = analyze_bite(0, len(data)*1.0/fs, data, fs)
        f = p[1]
        T = p[0]
        ET.add_map(f, T, fname)
    return fs, data


for i,ep in enumerate(episodes):
    add_file('sound/'+ep+'.wav')
    pct = (i+1)*1.0/len(episodes)*100
    print "%i %% done...\n" % (pct)
    
ET.save()



