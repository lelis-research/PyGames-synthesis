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
from src.Evaluation.evaluation import *
from src.Optimizer.optimizer import *
import time

class Plist:

    def __init__(self, constants=[], scalars=[], dsfs=[]):
        self.plist = {}
        
        for value in constants:
            const = Constant.new(value)
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

    def __init__(self, time_limit, logger, run_optimizer):
        self.time_limit = time_limit
        self.logger = logger
        self.run_optimizer = run_optimizer['run_optimizer']
        self.is_triage = run_optimizer['triage']
        self.kappa = run_optimizer['kappa']
        self.n_iter = run_optimizer['iterations']

    def synthesize(self, bound, operators, constants, scalars, 
                dsfs, eval_funct):
        """
        Implementation of Bottom-Up Search to synthesize program_decide_columns for
        the Catcher game
        """
        
        start = time.time()
        self.logger.set_start(start)
        self.closed_list = set()
        self.grammar = {}         
        
        self.grammar['operators'] = operators
        self.grammar['scalars'] = scalars
        self.grammar['constants'] = constants
        self.grammar['dsfs'] = dsfs
        
        self.plist = Plist(constants, scalars, dsfs)

        if self.run_optimizer:
            optimizer = Optimizer(eval_funct, self.is_triage, self.n_iter, self.kappa)

        number_of_evaluations = 0
        START_PROGRAM_EVAL = 1000
        for i in range(1, bound):
            self.logger.log('Exploring Programs of Size: ' + str(i))

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
                        pdescr = {'header': 'Evaluated Program', 'psize': arg.get_size(), 'score': res[1]}
                        self.logger.log_program(arg.to_string(), pdescr)
                        self.logger.log('Correct: ' + str(res[1]))

                        if res[1]:
                            const_param_values, score, is_optimized = optimizer.optimize(arg, res[0])
                            if is_optimized:
                                pdescr = {'header': 'Optimized Program', 'psize': arg.get_size(), 'score': score}
                                self.logger.log_program(arg.to_string(indent=1), pdescr)

                ppool = []

                end = time.time()
                if (end - start) > self.time_limit:
                    self.logger.log('Running Time: ' + str(round(end, 2)) + 'seconds')
                    return

            self.logger.log('Finished Exploring Programs of Size: ' + str(i))
            
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
