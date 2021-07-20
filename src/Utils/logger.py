"""
logger.py

Author: Olivier Vadiavaloo

Description:
This module defines a Logger class used to log results produced by the synthesizer
into a specified log file.
"""
import os
import datetime
import time
from os.path import join

class Logger:

    def __init__(self, log_file, algorithm, header_details):
        self.log_file = log_file
        self.log_dir = 'logs/'

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self.now = datetime.datetime.now()
        self.log_file += '-' + self.now.strftime("%d-%b-%Y--%H-%M")
        self.algorithm = algorithm
        self.header_details = header_details

    def log_details(self):
        print(f'{self.algorithm} Log - {self.now.strftime("%x %X")}')

        count = 0
        for detail_name, detail in self.header_details.items():
            print(f'{detail_name}: {detail}\t\t', end='')
            count += 1
            
            # Go to next line after printing 3 details
            if count == 3:
                print()

        print()

    def log_program(self, pstring, pdescr):
        header = pdescr.get('header')
        if header is None:
            header = 'Program Found'

        psize = pdescr.get('psize')
        if psize is None:
            psize = 'Not Specified'

        score = pdescr.get('score')
        if score is None:
            score = 'Not Specified'

        elapsed_time = pdescr.get('timestamp')
        if elapsed_time is None:
            elapsed_time = 'Not Specified'

        print('=' * 100)
        print(f'{header}\t Elapsed Time: {elapsed_time} mins')
        print('=' * 100)
        print(f'psize: {psize} \tscore: {score}\n')
        print(f'{pstring}\n')

    def log(self, item, end=''):

        if end is None:
            end = '\n'
        
        try:
            if type(item) is not str:
                item = str(item)
            
            print(item + end)
        except:
            raise Exception('Could not log item')