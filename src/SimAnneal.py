import numpy as np
import copy as cp
import random
from math import exp
from numpy.random import beta
from src.DSL import *
from src.Evaluation import *

class SimulatedAnnealing:

    def generate_random(self, grammar):
        pass

    def mutate(self, current):
        pass

    def reduce_temp(self, current_t):
        pass

    def is_accept(self, j_diff, temp):
        beta = 0.5
        rand = random.random()
        if rand < exp((j_diff * beta) / temp):
            return True
        return False

    def synthesize(self, grammar, current_t, final_t, eval_funct):
        best = self.generate_random(grammar)
        best_eval = eval_funct.evaluate(best)
        current, current_eval = best, best_eval

        while current_t > final_t:
            candidate = self.mutate(cp.deepcopy(current))
            candidate_eval = eval_funct.evaluate(current)
            if candidate_eval < best_eval:
                best, best_eval = candidate, candidate_eval
                print("New best:")
                print(best.toString())
                print("-" * 50)

            j_diff = current_eval - candidate_eval
            current_t = self.reduce_temp(current_t)
            
            if j_diff < 0 or self.is_accept(j_diff, current_t):
                current, current_eval = candidate, candidate_eval

        return best, best_eval