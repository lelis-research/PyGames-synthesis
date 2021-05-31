"""
BUS.py 

Author: Olivier Vadiavaloo

Description:
This module implements a Bottom-Up Search synthesizer for the 
generating strategies for playing the Catcher game from 
https://pygame-learning-environment.readthedocs.io/en/latest/user/games/catcher.html.

"""
from concurrent.futures import ProcessPoolExecutor
from .DSL import *
import time

class BUS:

    def init_plist(self):
        pass

    def synthesize(self, bound, operators, constants, scalars, 
                dsfs, eval_funct, programs_not_to_eval, start):
        """
        Implementation of Bottom-Up Search to synthesize program_decide_columns for
        the Can't Stop game
        """
        
        self.closed_list = set()
        self.grammar = {}         
        
        self.grammar['operators'] = operators
        self.grammar['scalars'] = scalars
        self.grammar['constants'] = constants
        self.grammar['dsfs'] = dsfs
        
        self.plist = self.init_plist()

        number_of_evaluations = 0
        START_PROGRAM_EVAL = 1000
        for i in range(1, bound):
            if i not in self.plist:
                self.plist[i] = []
                
            print('psize', i)
            number_of_programs = 0
            ppool = []
            for p in self.grow(i):
                number_of_evaluations += 1
                if p.toString() in programs_not_to_eval or type(p).__name__ != 'Argmax':
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
                            return arg

                ppool = []

                if (time.time() - start) > 1800:
                    print('timeout: 30 mins has elapsed\n')
                    return None

            print('Evaluations:', number_of_evaluations)
            print('----------')
        print()

        return None
            
    def grow(self, psize):
        nplist = []
        for op in self.grammar['operators']:
            for p in op.grow(self.plist.copy(), psize):
                if p.toString() not in self.closed_list:
                    self.closed_list.add(p.toString())
                    nplist.append(p)
                    yield p
        
        for p in nplist:
            self.plist[psize].append(p)

    def get_closed_list(self):
        return self.closed_list
