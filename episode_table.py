# -*- coding: utf-8 -*-
"""
Created on Mon Jun 02 15:54:51 2014

@author: dk122
"""
import cPickle as pickle
import os

class episode_table:
    def __init__(self, filename, mode='append'):
        self.filename = filename
        if os.path.isfile(filename) and mode=='append':
            table, names = pickle.load(open(filename, "rb"))
        else:
            table = dict()
            names = []
            
        self.hashtable  = table
        self.names      = names
        
        
    def __str__(self):
        self_as_string = 'Shows:'
        for show in self.names:
            self_as_string += '\t' + show + '\n'
        return self_as_string
        

    def add_map(self, f, T, name):
        for freq,time in zip(f,T):
            self.add_marker(freq,time,name)
    
    def add_marker(self, f, T, name):
        if not self.hashtable.has_key(f):
            self.hashtable[f] = []
        if not ([T, name] in self.hashtable[f]):            
            self.hashtable[f].append([T, name])
        if not (name in self.names):
            self.names.append(name)

    def save(self):
        pickle.dump([self.hashtable, self.names], open(self.filename, "wb"))