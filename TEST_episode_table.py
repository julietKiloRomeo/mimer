# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 11:58:58 2014

@author: dk122
"""

print '----------------------------------------------------------------------'

from episode_table import episode_table

ET = episode_table('test.pkl', mode = 'clear')

ET.add_marker(100.0, 1.1, 'Buffy')


ET.add_marker(100.0, 1.1, 'Buffy')

ET.add_marker(100.0, 1.1, 'Angel')
ET.add_marker(110.0, 10.1, 'Angel')

print 'Constructed:\n',
print ET

ET.save()

ET2 = episode_table('test.pkl')

print 'Loaded:\n',
print ET2

ET3 = episode_table('test.pkl', mode = 'clear')

print 'Load with clear:\n',
print ET3
