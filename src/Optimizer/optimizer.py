"""
optimizer.py

Author: Olivier Vadiavaloo

Description:
This module provides an Optimizer class that can be used by 
synthesizers such as Bottom-Up Search to find the optimal value
of operands/parameters in operations defined in the DSL.
"""
from numpy.lib.arraysetops import isin
from src.dsl import *
from src.evaluation import Evaluation
from scipy import spatial
from bayes_opt import BayesianOptimization
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
import numpy as np
import os

class Optimizer:

    def __init__(self, eval_funct, is_triage):
        self.eval_funct = eval_funct
        self.is_triage = is_triage
        self.log_file = './logs.json'

    def get_const_range(self):
        pbounds = {}
        original_values = []
        i = 1
        queue = []
        queue.append(self.tree)
        while len(queue) > 0:
            node = queue.pop(0)
            if isinstance(node, VarFromArray) or isinstance(node, VarScalar):
                continue

            if isinstance(node, Constant):
                node_name = 'Const' + str(i)
                i += 1
                original_values.append(node)
                interval = (node.get_children()[0] - 0.1, node.get_children()[0] + 0.1)
                pbounds[node_name] = interval
            
            else:
                for child in node.get_children():
                    queue.append(child)

        return pbounds, original_values

    def set_const_value(self, values):
        queue = []
        i = 1
        queue.append(self.tree)
        while len(queue) > 0:
            node = queue.pop(0)

            if isinstance(node, Constant):
                node_name = 'Const' + str(i)
                i += 1

                if type(values) is list:
                    node.replace_child(values.pop(0), 0)
                else:
                    node.replace_child(values[node_name], 0)
            
            else:
                for child in node.get_children():
                    queue.append(child)
        return

    def evaluation_fun(self, **kwargs):
        const_nodes = np.fromiter(kwargs.values(), dtype=float)
        self.set_const_value(const_nodes.tolist())
        score = self.eval_funct.evaluate(self.ast)
        return score

    def optimize(self, ast, initial_ast_score):
        self.ast = ast

        const_range_list, original_values = self.get_const_range()
        if len(original_values) == 0:
            return original_values, False

        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        else:
            print(f'{self.log_file} does not exist')

        bayesOpt = BayesianOptimization(
            self.evaluation_fun,
            pbounds=const_range_list,
            verbose=0
        )

        logger = JSONLogger(path=self.log_file)
        bayesOpt.subscribe(Events.OPTIMIZATION_STEP, logger)

        try:
            # Perform triage-based optimization if is_triage set to True
            current_score = initial_ast_score
            if self.is_triage:
                for n in [5, 10, 25, 60, 100]:
                    bayesOpt.maximize(init_points=20, n_iter=n)
                    assert bayesOpt.max['target'] < current_score
                    load_logs(bayesOpt, logs=[self.log_file])
            else:
                bayesOpt.maximize(init_points=20, n_iter=200)
            
            self.set_const_value(bayesOpt.max['params'])
            return bayesOpt.max['params'], True
        except:
            self.set_const_value(original_values)
            return original_values, False