# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 11:41:28 2014

@author: dk122
"""
import os
os.system('cls')


from scipy.io import wavfile
from constellation import analyze_bite
from episode_table import episode_table
from time import time
import numpy as np
import pylab as plt
from soundplayer import play
from threading import Thread



# load table
ET = episode_table('test_DB.pkl')

# load file

#testfile    = 'sound/seinfeld_percentage.wav' 
#testfile    = 'sound/seinfeld_doubledip.wav'
testfile    = 'sound/south_park_ask_mr_hat.wav'
#testfile    = 'sound/batman_ordinary.wav'



delay       = 1.951
SNR         = 0.8
fs, data    = wavfile.read(testfile)


P_data      = np.sum(data**2)*1.0/len(data)
noise       = np.random.normal(0, 1, data.shape)

P_noise     = np.sum(noise**2)/len(noise)

data        = P_data*( SNR*data/P_data + (1-SNR)*noise/P_noise)



def printname(p):
    (p,f) = os.path.split(p)
    (n,e) = os.path.splitext(f)
    return n


print "Testing with %s at a %2.1f s delay...\n" % (printname(testfile), delay)


def play_episode(data, fs):
    play(data, fs)


def process():

    t0 = time()
    
    
    ep_matches = dict()
    
    T_win = 1
    for i_start in range(int(np.ceil(delay*fs)), len(data)-T_win*fs, 256):
        T_start = i_start*1.0/fs
        p, cwt, FT = analyze_bite(T_start, T_win, data, fs)
        for T_real, f in zip(p[0] + T_start - delay, p[1]):
            f = round(f)
            if f in ET.hashtable.keys():
                matches = ET.hashtable[f]
                for match in matches:
                    T = match[0]
                    ep = match[1]
                    if not ep_matches.has_key(ep):
                        ep_matches[ep] = [[],[]]
                    ep_matches[ep][0].append(T_real)
                    ep_matches[ep][1].append(T)
    
    
    N_hits = []
    for i,ep in enumerate(ep_matches.keys()):
        N_hits.append(-len(ep_matches[ep][0]))
    
    
    
    sorted_idx = np.argsort(N_hits)
    for idx in sorted_idx:
        ep = ep_matches.keys()[idx]
#        N = len(ep_matches[ep][0])
    #    print "%8d %-30s" % (N, ep)
    
    
    guess_episode   = ep_matches.keys()[sorted_idx[0]]
    
    print "You were watching %s " % (printname(guess_episode)),
    
    
    #
    #print ep_matches.keys()
    
    dT = []
    X = []
    Y = []
    for (x,y) in zip(ep_matches[testfile][0],ep_matches[testfile][1]):
        X.append(x)
        Y.append(y)
        dT.append(y-x)
    
    
    median_offset = np.median(dT)
    
    t_elapsed   = time() - t0
    t_file      = len(data)/fs
    
    
    print "with a %2.1f s delay\n" % (median_offset)
    print "%3.1f s file took %3.1f s to process.\n" % (t_file, t_elapsed)
    
    return X,Y,dT
    
    
def draw(X,Y,dT):    
    plt.close('all')
    fig, axarr = plt.subplots(1,2, figsize=(20,18))
    axarr[0].plot(X,Y,'o', color=(1,0.1,0.1,0.4), markersize=12)   
    axarr[1].hist(dT)
    
    
if __name__ == '__main__':
    
    thread1 = Thread(target = play_episode, args = (data, fs,))
    thread2 = Thread(target = process)

    thread2.start()
    thread1.start()

    thread2.join()    
    thread1.join()    

