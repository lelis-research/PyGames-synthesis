"""
probe.py

Author: Olivier Vadiavaloo

Description:
This module implements the Probe algorithm and a data structure
for holding the bank of programs during the execution of the Probe
algorithm.
"""
from math import floor, log10
from src.dsl import *
from src.PROBE.rule import *
import itertools
import time

probability_key = 'probability'
cost_key = 'cost'

class Plist:

    def __init__(self, pcfg={}):
        self.plist = {}
        
        constants = pcfg['constants']
        scalars = pcfg['scalars']
        dsfs = pcfg['dsfs']
        
        for value in constants:
            const = Constant.new(value)
            self.insert(const, pcfg[const_rule][cost_key])

        for scalar in scalars:
            if isinstance(scalar, VarScalar):
                cost = pcfg[var_scalar_rule][cost_key]
            else:
                cost = pcfg[var_from_arr_rule][cost_key]
            self.insert(scalar, cost)

        for dsf in dsfs:
            p = dsf()
            if isinstance(p, FallingFruitPosition):
                cost = pcfg[fruit_pos_rule][cost_key]
            else:
                cost = pcfg[player_pos_rule][cost_key]
            self.insert(p, cost)
        
    def insert(self, item, cost):
        if self.plist.get(cost) is None:
            self.plist[cost] = {}
            self.plist[cost][type(item).__name__] = []
            self.plist[cost][type(item).__name__].append(item)
            return
        
        if self.plist[cost].get(type(item).__name__) is None:
            self.plist[cost][type(item).__name__] = []
        
        self.plist[cost][type(item).__name__].append(item)

    def get(self, cost, ptype=None):
        if ptype is None:
            return self.plist.get(cost)

        if self.plist.get(cost) is not None:
            return self.plist[cost].get(ptype)
        
        return None

    def copy(self):
        newPlist = Plist()
        newPlist.plist = self.plist.copy()
        return newPlist

class Probe:

    def select(self, partial_solutions, best_score):
        select_partial_solutions = []
        for p in partial_solutions:

            if self.eval[p.to_string()] > self.beta * (best_score + 1):
                select_partial_solutions.append(p)

        return select_partial_solutions

    def update(self, partial_solutions, best_score):
        normalization_factor = 0
        for rule in self.rules:
            fit = []
            for p in partial_solutions:
                if rule.used_in(p):
                    fit_value = (best_score + 1 - self.eval[p.to_string()]) / ((1 - self.beta) * (best_score + 1))
                    fit.append(fit_value)

            if len(fit) > 0:
                min_fit = min(fit)
            else:
                min_fit = 1

            self.pcfg[rule][probability_key] = self.pcfg[rule][probability_key] ** min_fit
            normalization_factor += self.pcfg[rule][probability_key]

        # Normalize costs of each rule
        for rule in self.rules:
            self.pcfg[rule][probability_key] /= normalization_factor

            # cost = - log ( Pr(R) )
            cost = floor(-1 * log10(self.pcfg[rule][probability_key]))
            self.pcfg[rule][cost_key] = max(1, cost)

    def probe(self, pcfg, rules, eval_funct, time_limit, logger):
        start = time.time()
        self.logger = logger
        self.logger.set_start(start)

        self.pcfg = pcfg
        self.rules = rules
        self.eval_funct = eval_funct
        self.cost_limit = 8
        self.beta = 0.55
        
        while time.time() - start < time_limit:
            best_program, best_program_cost, best_score, partial_solutions = self.guided_search()
            partial_solutions = self.select(partial_solutions, best_score)
            self.logger.log('partial_solutions\t' + str(partial_solutions))

            if len(partial_solutions) > 0:
                self.update(partial_solutions, best_score)

                for rule, value in self.pcfg.items():
                    if isinstance(rule, Rule):
                        self.logger.log(rule.top_symbol.className() + ', ' + str(value))

            if best_program is not None:
                pdescr = {
                    'header': 'Best Program After 1 iteration of PROBE',
                    'psize': best_program.get_size(),
                    'score': best_score
                }

                self.logger.log_program(best_program.to_string(), pdescr)
                self.logger.log('Program Cost: ' + str(best_program_cost), end='\n\n')

    def guided_search(self):
        cost = 1
        self.plist = Plist(pcfg=self.pcfg)
        current_best = None
        current_best_cost = -1
        current_best_score = -1_000_000
        partial_solutions = []
        self.eval = {}

        while cost <= self.cost_limit:
            for p in self.new_programs(cost):
                print(p.to_string())

                pstring = p.to_string()
                if self.eval.get(pstring) is not None:
                    continue

                if isinstance(p, (IT, ITE, Strategy, ReturnAction)):
                    pscore = self.eval_funct.evaluate(p)
                else:
                    pscore = -1_000_000
                psize = p.get_size()

                if pscore > current_best_score:
                    current_best = p
                    current_best_cost = cost
                    current_best_score = pscore

                    # Log new best program to file
                    pdescr = {'header': 'New Best Program', 'psize': psize, 'score': pscore}
                    self.logger.log_program(pstring, pdescr)
                    self.logger.log('Program Cost: ' + str(cost), end='\n\n')

                elif pscore > 0:
                    # A program is a partial solution if it has a positive score 
                    partial_solutions.append(p)

                    # Log partial solution to file
                    pdescr = {'header': 'Partial Solution', 'psize': psize, 'score': pscore}
                    self.logger.log_program(pstring, pdescr)
                    self.logger.log('Program Cost: ' + str(cost), end='\n\n')

                self.plist.insert(p, cost)
                self.eval[pstring] = pscore

            cost += 1

        return current_best, current_best_cost, current_best_score, partial_solutions.copy()

    def new_programs(self, cost):
        for rule in self.rules:
            if self.pcfg[rule][cost_key] == cost and rule.get_subexpr_count() == 0:
                yield rule.build_expression([])

            elif self.pcfg[rule][cost_key] < cost and rule.get_subexpr_count() > 0:

                cost_combinations = itertools.product(range(cost - self.pcfg[rule][cost_key] + 1), repeat=rule.get_subexpr_count())

                # print(cost - self.pcfg[rule]['cost'])
                # print(rule.top_symbol.className())
                
                for c in cost_combinations:
                    print(c)
                    if sum(c) + self.pcfg[rule][cost_key] == cost:
                        # print('true')
                        subexpr_list = []
                        for i in range(rule.get_subexpr_count()):
                            subexpr_list.append(list(rule.get_subexpr(i)))

                        # print('subexpr_list', subexpr_list)
                        subexpr_combinations = itertools.product(*subexpr_list)

                        for valid_subexpr in subexpr_combinations:
                            # print(valid_subexpr)
                            programs = []
                            for i in range(len(valid_subexpr)):
                                # Get list of all valid programs for each sub-expression
                                programs.append(self.plist.get(c[i], ptype=valid_subexpr[i].__name__))

                            if None in programs:
                                continue

                            # Cross-product of valid programs for each sub-expression
                            p_combinations = itertools.product(*programs)
                            for p_combination in p_combinations:
                                # print(p_combination)
                                p = rule.build_expression(list(p_combination))
                                yield p


# if __name__ == '__main__':

#     p = Strategy.new(
#         IT.new(GreaterThan.new(Constant.new(5), Constant.new(10)), ReturnAction.new(VarFromArray.new('actions', Constant.new(0)))),
#         None
#     )
#     print(gt_rule.used_in(p))
#     partial_solutions = [p]
    
#     syn = Probe()
#     syn.rules = [
#         ite_rule,
#         it_rule,
#         strategy_rule,
#         ra_rule,
#         plus_rule,
#         minus_rule,
#         times_rule,
#         divide_rule,
#         gt_rule,
#         lt_rule,
#         eq_rule,
#         var_scalar_rule,
#         var_from_arr_rule,
#         fruit_pos_rule,
#         player_pos_rule,
#         const_rule
#     ]
    
#     uniform_prob = 1 / len(syn.rules)
#     print(uniform_prob)
#     uniform_cost = floor(-1 * log10(uniform_prob))
#     print(uniform_cost)
#     input()

#     pcfg = {}

#     for rule in syn.rules:
#         pcfg[rule] = {probability_key: uniform_prob, cost_key: uniform_cost}

#     pcfg['dsfs'] = [FallingFruitPosition, PlayerPosition]
#     pcfg['constants'] = [0.5, 2]
#     pcfg['scalars'] = [
#         VarScalar.new('paddle_width'),
#         VarFromArray.new('actions', 0),
#         VarFromArray.new('actions', 1),
#         VarFromArray.new('actions', 2)
#     ]

#     syn.pcfg = pcfg
#     syn.eval = {}
#     syn.eval[p.to_string()] = 900
#     syn.beta = 0.50

#     syn.update(partial_solutions, 1000)
    
#     prob_sum = 0
#     for rule, prob in syn.pcfg.items():
#         if isinstance(rule, Rule):
#             print(rule.top_symbol.className(), prob)
#             prob_sum += prob[probability_key]
#     print(prob_sum)

# if __name__ == '__main__':

#     syn = Probe()
#     syn.rules = [
#         ite_rule,
#         it_rule,
#         strategy_rule,
#         ra_rule,
#         plus_rule,
#         minus_rule,
#         times_rule,
#         divide_rule,
#         gt_rule,
#         lt_rule,
#         eq_rule,
#         var_scalar_rule,
#         var_from_arr_rule,
#         fruit_pos_rule,
#         player_pos_rule,
#         const_rule
#     ]
    
#     uniform_prob = 1 / len(syn.rules)
#     print(uniform_prob)
#     uniform_cost = floor(-1 * log10(uniform_prob))
#     print(uniform_cost)
#     input()

#     pcfg = {}

#     for rule in syn.rules:
#         pcfg[rule] = {'probabilty': uniform_prob, 'cost': uniform_cost}

#     # syn.rules = [ra_rule]
#     # pcfg[it_rule] = {'probability': 0.01, 'cost': 1}
#     # pcfg[const_rule] = {'probability': 0.01, 'cost': 1}
#     # pcfg[var_from_arr_rule] = {'probability': 0.01, 'cost': 1}
#     # pcfg[var_scalar_rule] = {'probability': 0.01, 'cost': 1}
#     # pcfg[fruit_pos_rule] = {'probability': 0.01, 'cost': 1}
#     # pcfg[player_pos_rule] = {'probability': 0.01, 'cost': 1}
#     # pcfg[ra_rule] = {'probability': 0.01, 'cost': 1}

#     pcfg['dsfs'] = [FallingFruitPosition, PlayerPosition]
#     pcfg['constants'] = [0.5, 2]
#     pcfg['scalars'] = [
#         VarScalar.new('paddle_width'),
#         VarFromArray.new('actions', 0),
#         VarFromArray.new('actions', 1),
#         VarFromArray.new('actions', 2)
#     ]

#     # syn.rules = [plus_rule]
#     # pcfg[plus_rule] = {'probability': 0.05, 'cost': 2}
#     # pcfg[it_rule] = {'probability': 0.05, 'cost': 1}
#     # pcfg[ra_rule] = {'probability': 0.06, 'cost': 1}
#     # pcfg[const_rule] = {'probability': 0.03, 'cost': 1}
#     # pcfg[var_scalar_rule] = {'probability': 0.03, 'cost': 1}
#     # pcfg[var_from_arr_rule] = {'probability': 0.03, 'cost': 1}
#     # pcfg[fruit_pos_rule] = {'probability': 0.03, 'cost': 1}
#     # pcfg[player_pos_rule] = {'probability': 0.03, 'cost': 1}

#     syn.pcfg = pcfg

#     syn.plist = Plist(pcfg)
#     print(syn.plist.plist)

#     # syn.plist.insert(GreaterThan.new(Constant.new(0.5), Constant.new(2)), 3)
#     # syn.plist.insert(ReturnAction.new(VarFromArray.new('actions', 0)), 2)

#     for i in range(2, 8):
#         for p in syn.new_programs(i):
#             if isinstance(p, IT):
#                 print('i', i)
#                 print(p.to_string())
#                 input()
#             syn.plist.insert(p, i)

#     # for p in syn.new_programs(2):
#     #      print(p.to_string())