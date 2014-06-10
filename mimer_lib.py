# -*- coding: utf-8 -*-
"""
Created on Sun Jun 08 14:02:37 2014

@author: dk122
"""



from constellation import analyze_bite
from episode_table import episode_table
import numpy as np
from scipy.optimize import curve_fit
from scipy import stats
import os

def straigh_line(x, a):
    return a + x

def printname(p):
    (p,f) = os.path.split(p)
    (n,e) = os.path.splitext(f)
    return n

class mimer:
    def __init__(self, fs):
        # load table
        self.db = episode_table('test_DB.pkl')
        self.fs = fs
        
    def T_to_idx(self, T):
        return int(T*self.fs)
    def idx_to_T(self, idx):
        return idx*1.0/self.fs

    def process(self, data, T_win=1):        
        # init dict with matching episodes
        ep_matches = dict()
        
        # get length of time window to analyze per iteration
        N_win   = self.T_to_idx(T_win)
        N_data  = len(data)
        # step with 1/4 window size
        N_step  = N_win//4
        # loop over windows in input sound
        for i_start in range(0, N_data - self.T_to_idx(T_win), N_step):
            T_start = self.idx_to_T(i_start)
            # get short-time-fft and find peaks in spectogram
            peaks, im, FT_vectors = analyze_bite(T_start, T_win, data, self.fs)
            for T_real, f in zip(peaks[0] + T_start, peaks[1]):
                # round off the frequency
                f = round(f)
                if f in self.db.hashtable.keys():
                    matches = self.db.hashtable[f]
                    for match in matches:
                        T   = match[0]
                        ep  = match[1]
                        if not ep_matches.has_key(ep):
                            ep_matches[ep] = [[],[]]
                        ep_matches[ep][0].append(T_real)
                        ep_matches[ep][1].append(T)
        
        # sort by number of matches on episode name
        fitness = []
        output = []
        for ep in ep_matches.keys():
#            Corr    = np.corrcoef(ep_matches[ep][0],ep_matches[ep][1])
#            score   = Corr[0][1]
            dT      = [t1-t2 for (t1,t2) in zip(ep_matches[ep][1], ep_matches[ep][0])]
            T_est   = stats.mode(dT)[0][0]
            T_file  = np.array(ep_matches[ep][1])[abs(dT - T_est) < 1 ]
            T_win   = np.array(ep_matches[ep][0])[abs(dT - T_est) < 1 ]

            N       = len(T_file)
            score   = np.std(dT)
            
            popt, pcov = curve_fit(straigh_line, T_win, T_file)            
            
            if np.isinf(pcov):
                score       = 0.001
            else:
                score       = N*1.0/pcov[0][0]
            output.append([printname(ep), score, T_est, N, ep_matches[ep]])
            fitness.append(score)
                
        sorted_idx = np.argsort(fitness)
        sorted_out = [output[i] for i in sorted_idx]
        return sorted_out