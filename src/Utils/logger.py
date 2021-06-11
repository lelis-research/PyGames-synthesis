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
        self.start = None

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        now = datetime.datetime.now()
        self.log_file += '-' + now.strftime("%d-%b-%Y--%H-%M")
        self.create_header(algorithm, now, header_details)

    def set_start(self, start):
        assert type(start) is float
        self.start = start

    def create_header(self, algorithm, now, header_details):
        with open(join(self.log_dir + self.log_file), 'a') as p_file:
            p_file.write(f'{algorithm} Log - ')
            p_file.write(f'{now.strftime("%x %X")}\n')

            count = 0
            for detail_name, detail in header_details.items():
                p_file.write(f'{detail_name}: {detail}\t\t')
                count += 1
                
                # Go to next line after printing 3 details
                if count == 3:
                    p_file.write('\n')

            p_file.write('\n')

    def log_program(self, pstring, pdescr):
        if self.start is None:
            raise Exception('start attribute of Logger must be set')

        elapsed_time = round((time.time() - self.start), 2)
        
        header = pdescr.get('header')
        if header is None:
            header = 'Program Found'

        psize = pdescr.get('psize')
        if psize is None:
            psize = 'Not Specified'

        score = pdescr.get('score')
        if score is None:
            score = 'Not Specified'

        with open(join(self.log_dir + self.log_file), 'a') as p_file:
            p_file.write('=' * 100)
            p_file.write(f'\n{header}\t Elapsed Time: {elapsed_time} seconds\n')
            p_file.write('=' * 100)
            p_file.write(f'\npsize: {psize} \tscore: {score}\n\n')
            p_file.write(f'{pstring}\n\n')

    def log(self, item, end=None):

        if end is None:
            end = '\n'
        
        try:
            if type(item) is not str:
                item = str(item)
            
            with open(join(self.log_dir + self.log_file), 'a') as p_file:
                p_file.write(item + end)
        except:
            raise Exception('Could not log item')