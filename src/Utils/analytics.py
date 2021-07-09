"""
analytics.py

Author: Olivier Vadiavaloo

Description:
This module implements the Analytics class which provides handy statistics from
data obtained while running the synthesizer. The .dat files produced from calling
the save_data method of the plotter class can analyzed and the mean, std deviation
and the like can be returned.
"""
import os
from statistics import *

class Analytics:

    def __init__(self):
        pass

    def analyse_dat_file(self, filepath, name, var_num):
        assert os.path.exists(filepath)

        print('Stats for ', filepath)
        with open(filepath, 'r') as data_file:
            lines = data_file.readlines()

            for line in lines:
                if line[0] == '#':
                    continue
                
                split_line = line.split()
                var = split_line[int(var_num)]
                
                print(f'\tmean of {name}: ', mean(var))
                print(f'\tmedian of {name}:', median(var))
                print(f'\tvariance of {name}:', variance(var))
                print(f'\tstd. deviation of {name}:', stdev(var))