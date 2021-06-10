"""
sim_anneal.py

Author: Olivier Vadiavaloo

Description:
This file contains the code implementing the simulated annealing
algorithm.

"""
import numpy as np
import copy as cp
import time
import random
import os
import datetime
from math import exp
from numpy.random import beta, rand
from src.dsl import *
from src.evaluation import *
from os.path import join
from src.Optimizer.optimizer import *

class SimulatedAnnealing:

    def __init__(self, time_limit, log_file):
        self.time_limit = time_limit
        self.log_file = log_file
        self.log_dir = 'logs/'

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        now = datetime.datetime.now()
        self.log_file += '-' + now.strftime("%d-%b-%Y--%H-%M")

    def get_terminal_node(self, p, valid_ith_child_types):
        terminal_nodes = []

        for child_type in valid_ith_child_types:
            if child_type is None:
                terminal_nodes.append(child_type)
                continue

            child = Node.instance(child_type)
            if child_type in [VarFromArray.className(), VarScalar.className(), Constant.className()] \
                or child.get_max_number_children() == 0:
                terminal_nodes.append(child)

        if terminal_nodes == 0:
            for child_type in valid_ith_child_types:
                child = Node.instance(child_type)

                if child.get_max_children_number() == 1:
                    terminal_nodes.append(child)

        if len(terminal_nodes) > 0:
            return random.choice(terminal_nodes)

        return Node.instance(random.choice(list(valid_ith_child_types)))

    def complete_program(self, p, depth, max_depth):
        if p is None:
            return

        for i in range(p.get_max_number_children()):
            valid_ith_child_types = p.get_valid_children_types()[i]

            # if p is a scalar or constant, no need to call complete_program on child
            if isinstance(p, VarScalar) or isinstance(p, VarFromArray) or isinstance(p, Constant):
                child = random.choice(list(valid_ith_child_types))
                p.add_child(child)

            # if max depth is exceeded, get a terminal node
            elif depth >= max_depth:
                child = self.get_terminal_node(p, valid_ith_child_types)
                p.add_child(child)
                self.complete_program(child, depth+1, max_depth)

            # else choose a random child node
            else:
                child = Node.instance(random.choice(list(valid_ith_child_types)))
                p.add_child(child)
                self.complete_program(child, depth+1, max_depth)

    def generate_random(self):
        initial_nodes = Node.get_valid_children_types()[0]
        random_p = Node.instance(random.choice(list(initial_nodes)))
        self.complete_program(random_p, self.initial_depth, self.max_depth)
        random_p.check_correct_size()
        return random_p

    def mutate_inner_nodes(self, p, index):
        self.processed_nodes += 1

        if not isinstance(p, Node):
            return False

        for i in range(p.get_max_number_children()):

            if index == self.processed_nodes:
                valid_ith_child_types = p.get_valid_children_types()[i]
                
                child = Node.instance(random.choice(list(valid_ith_child_types)))

                if isinstance(child, Node):
                    self.complete_program(child, 0, 4)
                p.replace_child(child, i)

                return True

            if self.mutate_inner_nodes(p.get_children()[i], index):
                return True

        return False

    def mutate(self, p):
        # print('p.get_size()', p.get_size())
        index = random.randint(0, p.get_size())
        # print('index', index)
        # print()

        # root will be mutated
        if index == 0:
            ptypes = Node.get_valid_children_types()[0]
            p = Node.instance(random.choice(list(ptypes)))
            self.complete_program(p, 0, 4)
            p.check_correct_size()

            return p

        self.processed_nodes = 0
        self.mutate_inner_nodes(p, index)
        p.check_correct_size()

        return p

    def reduce_temp(self, current_t, epoch):
        return current_t / (1 + self.alpha * epoch)

    def is_accept(self, j_diff, temp):
        rand = random.uniform(0, 1)
        if rand < min(1, exp(j_diff * (self.beta / temp))):
            return True
        return False

    def init_var_child_types(self, grammar):
        VarFromArray.valid_children_types = [set(grammar['arrays']), set(grammar['array_indexes'])]
        VarScalar.valid_children_types = [set(grammar['scalars'])]
        Constant.valid_children_types = [set(grammar['constants'])]

    def synthesize(self, grammar, current_t, final_t, eval_funct):
        start = time.time()

        self.alpha = 0.9
        self.beta = 100
        self.initial_depth = 0
        self.max_depth = 4
        self.initial_t = current_t

        self.init_var_child_types(grammar)

        best = None
        best_eval = None

        self.optimizer = Optimizer(eval_funct, False)

        while time.time() - start < self.time_limit:
            current_t = self.initial_t

            current = self.generate_random()
            current_eval = eval_funct.evaluate(best)

            if best is None or current_eval > best_eval:
                best, best_eval = current, current_eval

            epoch = 0
            while current_t > final_t:
                candidate = self.mutate(cp.deepcopy(current))
                candidate_eval = eval_funct.evaluate(candidate)

                if candidate_eval > best_eval:
                    optimized_const_values, new_score, is_optimized = self.optimizer.optimize(candidate, candidate_eval)

                    if is_optimized:
                        candidate_eval = new_score

                    best, best_eval = candidate, candidate_eval
                    with open(join(self.log_dir + self.log_file), 'a') as best_p_file:
                        best_p_file.write('=' * 100)
                        best_p_file.write('\n')
                        best_p_file.write('New Best\n')
                        best_p_file.write('=' * 100)
                        best_p_file.write('\n')
                        best_p_file.write(f'psize: {candidate.get_size()}, pscore: {candidate_eval}\n')
                        best_p_file.write(f'\n{candidate.to_string()}\n')

                j_diff = candidate_eval - current_eval
                
                if j_diff > 0 or self.is_accept(j_diff, current_t):
                    current, current_eval = candidate, candidate_eval
                
                current_t = self.reduce_temp(current_t, epoch)
                epoch += 1

        print(time.time() - start)
        return best, best_eval