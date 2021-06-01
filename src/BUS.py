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
from DSL import *
# from Evaluation import *
import time

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
        if self.plist.get(item.getSize()) is None:
            self.plist[item.getSize()] = {}
            self.plist[item.getSize()][type(item).__name__] = []
            self.plist[item.getSize()][type(item).__name__].append(item)
            return
        
        if self.plist[item.getSize()].get(type(item).__name__) is None:
            self.plist[item.getSize()][type(item).__name__] = []
        
        self.plist[item.getSize()][type(item).__name__].append(item)

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
            print('-' * 10)         # print horizontal line
            print('psize', i)
            print('-' * 10)

            number_of_programs = 0
            ppool = []
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
                        print(f"{arg.toString()}, {res}")
                        if res:
                            return time.time() - start, arg

                ppool = []

                end = time.time()
                if (end - start) > 1800:
                    print('timeout: 30 mins has elapsed\n')
                    return end, None
        print()

        return time.time() - start, None
            
    def grow(self, psize):
        nplist = []
        for op in self.grammar['operators']:
            for p in op.grow(self.plist.copy(), psize):
                if p.toString() not in self.closed_list:
                    self.closed_list.add(p.toString())
                    nplist.append(p)
                    yield p
        
        for p in nplist:
            self.plist.insert(p)
