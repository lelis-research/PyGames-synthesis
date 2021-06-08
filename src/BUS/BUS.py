"""
BUS.py 

Author: Olivier Vadiavaloo

Description:
This module implements a Bottom-Up Search synthesizer for 
generating strategies for playing the Catcher game from 
https://pygame-learning-environment.readthedocs.io/en/latest/user/games/catcher.html.

The evaluation object is defined in the Evaluation module.

"""
from concurrent.futures import ProcessPoolExecutor
from src.BUS.bus_dsl import *
from src.evaluation import *
from os.path import join
import time
import os
import datetime

class Plist:

    def __init__(self, constants=[], scalars=[], dsfs=[]):
        self.plist = {}
        
        for const in constants:
            self.insert(const)

        for scalar in scalars:
            self.insert(scalar)

        for dsf in dsfs:
            p = dsf()
            self.insert(p)
        
    def insert(self, item):
        if self.plist.get(item.get_size()) is None:
            self.plist[item.get_size()] = {}
            self.plist[item.get_size()][type(item).__name__] = []
            self.plist[item.get_size()][type(item).__name__].append(item)
            return
        
        if self.plist[item.get_size()].get(type(item).__name__) is None:
            self.plist[item.get_size()][type(item).__name__] = []
        
        self.plist[item.get_size()][type(item).__name__].append(item)

    def get(self, size, ptype=None):
        if ptype is None:
            return self.plist.get(size)

        if self.plist.get(size) is not None:
            return self.plist[size].get(ptype)
        
        return None

    def copy(self):
        newPlist = Plist()
        newPlist.plist = self.plist.copy()
        return newPlist


class BUS:

    def __init__(self, time_limit, log_file):
        self.time_limit = time_limit
        self.log_file = log_file
        self.log_dir = 'logs/'

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        now = datetime.datetime.now()
        self.log_file += "-" + now.strftime("%d-%b-%Y--%H:%M")

    def synthesize(self, bound, operators, constants, scalars, 
                dsfs, eval_funct):
        """
        Implementation of Bottom-Up Search to synthesize program_decide_columns for
        the Can't Stop game
        """
        
        start = time.time()
        self.closed_list = set()
        self.grammar = {}         
        
        self.grammar['operators'] = operators
        self.grammar['scalars'] = scalars
        self.grammar['constants'] = constants
        self.grammar['dsfs'] = dsfs
        
        self.plist = Plist(constants, scalars, dsfs)

        number_of_evaluations = 0
        START_PROGRAM_EVAL = 1000
        for i in range(1, bound):
            with open(join(self.log_dir + self.log_file), "a") as p_file:
                p_file.write(f'psize {i}')
                p_file.write('_' * 100)

            for p in self.grow(i):
                number_of_evaluations += 1
                if type(p).__name__ != 'Strategy':
                    continue

                ppool.append(p)
                if number_of_programs < START_PROGRAM_EVAL:
                    number_of_programs += 1
                    continue

                number_of_programs = 0

                # if eval_funct.is_correct(p):
                #     print('Evaluations:', number_of_evaluations)
                #     return p

                with ProcessPoolExecutor() as executor:
                    for arg, res in zip(ppool, executor.map(eval_funct.is_correct, ppool, chunksize=5)):
                        
                        with open(join(self.log_dir + self.log_file), "a") as p_file:
                            p_file.write('=' * 100)
                            p_file.write(f'psize: {arg.get_size()}, is_correct: {res}')
                            p_file.write('=' * 100)
                            p_file.write(arg.to_string())

                        if res:
                            return time.time() - start, arg

                ppool = []

                end = time.time()
                if (end - start) > self.time_limit:
                    print(f'timeout: {self.time_limit // 3600} hours have elapsed\n')
                    return end, None
        print()

        return time.time() - start, None
            
    def grow(self, psize):
        nplist = []
        for op in self.grammar['operators']:
            for p in op.grow(self.plist.copy(), psize):
                if p.to_string() not in self.closed_list:
                    self.closed_list.add(p.to_string())
                    nplist.append(p)
                    yield p
        
        for p in nplist:
            self.plist.insert(p)
