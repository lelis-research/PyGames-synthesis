"""
sim_anneal.py

Author: Olivier Vadiavaloo

Description:
This file contains the code implementing the simulated annealing
algorithm.

"""
import numpy as np
import copy as cp
import random
from math import exp
from numpy.random import beta, rand
from src.dsl import *
from src.evaluation import *

class SimulatedAnnealing:

    def get_terminal_node(self, p, valid_ith_child_types):
        terminal_nodes = []

        for child_type in valid_ith_child_types:
            child = child_type()
            if child_type.className() in [VarFromArray.className(), VarScalar.className(), Constant.className()] \
                or child.get_max_children_number() == 0:
                terminal_nodes.append(child)

        if terminal_nodes == 0:
            for child_type in valid_ith_child_types:
                child = child_type()
                if child.get_max_children_number() == 1:
                    terminal_nodes.append(child)

        if len(terminal_nodes) > 0:
            return random.choice(terminal_nodes)

        return random.choice(list(valid_ith_child_types))

    def complete_program(self, p, depth, max_depth): 
        for i in range(p.get_max_number_children()):
            valid_ith_child_types = p.get_valid_children_types()[i]

            # if p is a scalar or constant, no need to call complete_program on child
            if isinstance(p, VarScalar) or isinstance(p, VarFromArray) or isinstance(p, Constant):
                child = random.choice(list(valid_ith_child_types))()
                p.add_child(child)

            # if max depth is exceeded, get a terminal node
            elif depth >= max_depth:
                child = self.get_terminal_node(p, valid_ith_child_types)
                p.add_child(child)

            # else choose a random child node
            else:
                child = random.choice(list(valid_ith_child_types))
                p.add_child(child)
                self.complete_program(child, depth+1, max_depth)

    def generate_random(self, grammar):
        initial_nodes = Node.get_valid_children_types()[0]
        random_p_class = random.choice(list(initial_nodes))
        random_p = random_p_class()
        self.complete_program(random_p, self.initial_depth, self.max_depth)
        return random_p

    def mutate_inner_nodes(self, p, index):
        self.processed_nodes += 1

        for i in range(p.get_max_number_children()):

            if index == self.processed_nodes:
                valid_ith_child_types = p.get_valid_children_types()[i]
                
                child = random.choice(list(valid_ith_child_types))
                self.complete_program(child, 0, 4)
                p.replace_child(child, i)

                return True

            return self.mutate_inner_nodes(p.get_children()[i], index)

        return False


    def mutate(self, p):
        index = random.randrange(p.getSize())

        # root will be mutated
        if index == 0:
            ptypes = Node.get_valid_children_types()[0]
            p = random.choice(list(ptypes))()
            self.complete_program(p, 0, 4)

            return p

        self.processed_nodes = 0
        self.mutate_inner_nodes(p, index)

        return p

    def reduce_temp(self, current_t, epoch):
        return current_t / (1 + self.alpha * epoch)

    def is_accept(self, j_diff, temp):
        rand = random.random()
        if rand < exp(j_diff * (self.beta / temp)):
            return True
        return False

    def synthesize(self, grammar, current_t, final_t, eval_funct):
        best = self.generate_random(grammar)
        best_eval = eval_funct.evaluate(best)
        current, current_eval = best, best_eval

        self.alpha = 0.9
        self.beta = 100
        self.initial_depth = 0
        self.max_depth = 4

        epoch = 0
        while current_t > final_t:
            candidate = self.mutate(cp.deepcopy(current))
            candidate_eval = eval_funct.evaluate(current)
            if candidate_eval < best_eval:
                best, best_eval = candidate, candidate_eval
                print("New best:")
                print(best.toString())
                print("-" * 50)

            j_diff = current_eval - candidate_eval
            
            if j_diff < 0 or self.is_accept(j_diff, current_t):
                current, current_eval = candidate, candidate_eval
            
            current_t = self.reduce_temp(current_t, epoch)
            epoch += 1

        return best, best_eval