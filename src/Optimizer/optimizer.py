"""
optimizer.py

Author: Olivier Vadiavaloo

Description:
This module provides an Optimizer class that can be used by 
synthesizers such as Bottom-Up Search to find the optimal value
of operands/parameters in operations defined in the DSL.
"""
from bayes_opt import BayesianOptimization, UtilityFunction
from src.dsl import *
import numpy as np
import math

class Optimizer:

    def __init__(self, eval_funct, is_triage, iterations, kappa):
        self.eval_funct = eval_funct
        self.is_triage = is_triage
        self.iterations = iterations
        self.kappa = kappa
        if is_triage:
            self.iter_breakdown = self.break_down(iterations)

    def set_baseline_eval(self, baseline_eval):
        self.baseline_eval = baseline_eval

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
                original_values.append(node.get_children()[0])
                interval = (0.001, 100.001)
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
        scores, target = self.eval_funct.evaluate(self.ast, verbose=True)
        self.all_scores[self.ast.to_string()] = scores

        return target

    def break_down(self, value):
        iter_breakdown = []
        for i in [21, 30, 49]:
            iter_breakdown.append(int((i / 100) * value))

        return iter_breakdown.copy()

    def triage_optimize(self):
        bayesOpt = BayesianOptimization(
            f=None,
            pbounds=self.const_range_list,
            verbose=0
        )

        def compute_epsilon(num_iterations):
            return 500 * math.sqrt(math.log(2 / (1 - math.sqrt(0.95))) / (2 * num_iterations))

        utility = UtilityFunction(kind='ucb', kappa=self.kappa, xi=0.0)

        current_eval = self.initial_score
        current_params = self.original_values
        all_scores = {}
        all_scores[self.ast.to_string()] = self.initial_scores

        is_optimized = False

        bayesOpt.register(params=current_params, target=current_eval)

        # Run Bayesian Optimization
        num_iterations = 0
        while num_iterations < self.iterations:
            next_point = bayesOpt.suggest(utility)
            self.set_const_value(next_point)
            scores, target = self.eval_funct.evaluate(self.ast, verbose=True)
            bayesOpt.register(params=next_point, target=target)
            num_iterations += 1

            all_scores[self.ast.to_string()] = scores

            current_eval, current_params = bayesOpt.max['target'], bayesOpt.max['params']

            epsilon = compute_epsilon(num_iterations)
            current_eval_ub = current_eval + epsilon

            baseline_epsilon = compute_epsilon(self.iterations)
            baseline_lb = self.baseline_eval - baseline_epsilon

            if current_eval_ub <= baseline_lb:
                break

        if current_eval > self.initial_score:
            is_optimized = True

        self.set_const_value(current_params)
        return self.ast, current_params, current_eval, all_scores[self.ast.to_string()], is_optimized

    def non_triage_optimize(self):
        bayesOpt = BayesianOptimization(
            f=self.evaluation_fun,
            pbounds=self.const_range_list,
            verbose=0
        )

        is_optimized = False
        self.all_scores = {}
        self.all_scores[self.ast.to_string()] = self.initial_scores

        bayesOpt.maximize(init_points=20, n_iter=self.iterations, kappa=self.kappa)
        target, params = bayesOpt.max['target'], bayesOpt.max['params']

        if target > self.initial_score:
            is_optimized = True

        self.set_const_value(params)
        return self.ast, params, target, self.all_scores[self.ast.to_string()], is_optimized

    def optimize(self, ast, initial_ast_score, initial_ast_scores):
        self.ast = ast
        self.initial_score = initial_ast_score
        self.initial_scores = initial_ast_scores

        self.const_range_list, self.original_values = self.get_const_range()
        if len(self.original_values) == 0:
            return self.ast, self.original_values, initial_ast_score, initial_ast_scores, False

        try:
            if self.is_triage:
                return self.triage_optimize()
            else:
                return self.non_triage_optimize()
        except:
            self.set_const_value(self.original_values)
            return self.ast, self.original_values, self.initial_score, self.initial_scores, False