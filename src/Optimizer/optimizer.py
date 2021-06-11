"""
optimizer.py

Author: Olivier Vadiavaloo

Description:
This module provides an Optimizer class that can be used by 
synthesizers such as Bottom-Up Search to find the optimal value
of operands/parameters in operations defined in the DSL.
"""
from src.dsl import *
from src.evaluation import Evaluation
from bayes_opt import BayesianOptimization, UtilityFunction
import numpy as np

class Optimizer:

    def __init__(self, eval_funct, is_triage, iterations, kappa):
        self.eval_funct = eval_funct
        self.is_triage = is_triage
        self.iterations = iterations
        self.kappa = kappa
        if is_triage:
            self.iter_breakdown = self.break_down(iterations)

    def get_const_range(self):
        pbounds = {}
        original_values = []
        i = 1
        queue = []
        queue.append(self.ast)
        while len(queue) > 0:
            node = queue.pop(0)
            if isinstance(node, VarFromArray) or isinstance(node, VarScalar):
                continue

            if isinstance(node, Constant):
                node_name = 'Const' + str(i)
                i += 1
                original_values.append(node)
                interval = (node.get_children()[0] - 10, node.get_children()[0] + 10)
                pbounds[node_name] = interval
            
            else:
                if isinstance(node, Node):
                    for child in node.get_children():
                        queue.append(child)

        return pbounds, original_values

    def set_const_value(self, values):
        queue = []
        i = 1
        queue.append(self.ast)
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
                if isinstance(node, Node):
                    for child in node.get_children():
                        queue.append(child)
        return

    def evaluation_fun(self, **kwargs):
        const_nodes = np.fromiter(kwargs.values(), dtype=float)
        self.set_const_value(const_nodes.tolist())
        score = self.eval_funct.evaluate(self.ast)
        return score

    def break_down(self, iterations):
        iter_breakdown = []
        for i in [1, 5, 15, 30, 49]:
            iter_breakdown.append(int((i / 100) * iterations))

        return iter_breakdown.copy()

    def triage_optimize(self):
        bayesOpt = BayesianOptimization(
            f=None,
            pbounds=self.const_range_list,
            verbose=0
        )

        utility = UtilityFunction(kind='ucb', kappa=self.kappa, xi=0.0)

        current_max_score = self.initial_score
        current_argmax_params = self.original_values
        is_optimized = True
        for i in self.iter_breakdown:
            # Run Bayesian Optimization
            for _ in range(i):
                next_point = bayesOpt.suggest(utility)
                target = self.evaluation_fun(next_point)
                bayesOpt.register(params=next_point, target=target)

            # Compare results with previous runs of the optimizer
            target, params = bayesOpt.max['target'], bayesOpt.max['params']
            if target < current_max_score:
                is_optimized = False
                break

            current_max_score = target
            current_argmax_params = params

        self.set_const_value(current_argmax_params)
        return current_argmax_params, current_max_score, is_optimized

    def non_triage_optimize(self):
        bayesOpt = BayesianOptimization(
            f=self.evaluation_fun,
            pbounds=self.const_range_list,
            verbose=0
        )

        bayesOpt.maximize(init_points=20, n_iter=self.iterations, kappa=self.kappa)
        target, params = bayesOpt.max['target'], bayesOpt.max['params']
        if target < self.initial_score:
            is_optimized = False
            params = self.original_values
            target = self.initial_score

        self.set_const_value(params)
        return bayesOpt.max['params'], bayesOpt.max['target'], is_optimized

    def optimize(self, ast, initial_ast_score):
        self.ast = ast
        self.initial_score = initial_ast_score

        self.const_range_list, self.original_values = self.get_const_range()
        if len(self.original_values) == 0:
            return self.original_values, 0, False

        try:
            if self.is_triage:
                return self.triage_optimize()
            else:
                return self.non_triage_optimize()
        except:
            self.set_const_value(self.original_values)
            return self.original_values, self.initial_score, False