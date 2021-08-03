"""
evalution_config_parent.py

Author: Olivier Vadiavaloo

Description:
This file implements the parent class, EvaluationConfig.
The EvaluationConfig class encapsulates the configuration to use during the evalution
phase of the synthesis process. An example of a configuration that could be used is
batch evaluation with triage, where the program is evaluated in batches of games, 
the maximum score of each batch is averaged out and this average is then used to gauge
the generated program's performance.

The EvaluationConfig class is used by the Evaluation class which implements the evaluation
logic at a higher level.
"""
from statistics import *
import math

class EvaluationConfig:

    total_games_name = 'total_games'
    best_eval_name = 'best_eval'
    min_score_name = 'MIN_SCORE'
    triage_name = 'triage'
    batch_size_name = 'batch_size'
    confidence_value_name = 'confidence_value'
    triage_var_bound_name = 'triage_var_bound'

    def __init__(self, attributes):
        self.config_attributes_set = False
        self.set_config_attributes(attributes)

    def set_config_attributes(self, attributes):
        self.triage = attributes[self.triage_name]
        self.triage_confidence_value = attributes[self.confidence_value_name]
        self.triage_random_var_bound = attributes[self.triage_var_bound_name]
        self.total_games = attributes[self.total_games_name]
        self.best_eval = attributes[self.best_eval_name]
        self.MIN_SCORE = attributes[self.min_score_name]
        self.config_attributes_set = True
        self.clean_up()

    def set_triage(self, triage):
        old_value = self.triage
        self.triage = triage
        return old_value

    def get_triage(self):
        return self.triage

    def set_total_games(self, total_games):
        old_value = self.total_games
        self.total_games = total_games
        return old_value

    def get_total_games(self):
        return self.total_games

    def set_best_eval(self, best_eval):
        self.best_eval = best_eval

    def get_best_eval(self):
        return self.best_eval

    def get_random_var_bound(self):
        return self.triage_random_var_bound

    def get_confidence_value(self):
        return self.triage_confidence_value

    def clean_up(self):
        pass

    def compute_results(self, scores, games_played):
        raise Exception('Must implement compute_results method')

    def check_continue(self, program_current_score, games_played):
        raise Exception('Must implement check_continue method')

    def check_triage_stop(self, program_current_score, games_played):

        def compute_epsilon(number_evals):
            return self.triage_random_var_bound * \
                math.sqrt(math.log(2 / (1 - math.sqrt(self.triage_confidence_value))) / (2 * number_evals))

        epsilon_current_best = compute_epsilon(self.total_games)
        epsilon_program = compute_epsilon(games_played)

        # print('CI', self.triage_confidence_value)
        # print('random var bound', self.triage_random_var_bound)

        # print('games_played', games_played)
        # print('current best score', self.best_eval)
        # print('transform current best score', transform_current_best)
        # print('epsilon current best score', epsilon_current_best)
        # print('current best lower bound', self.best_eval - epsilon_current_best)
        # print('current best lower bound (x500)', self.best_eval - (epsilon_current_best * 500))
        # print('transform current best lb (100)', transform_current_best - (epsilon_current_best * 100))
        # print()

        # print('program score', program_current_score)
        # print('transform program score', transform_program_curr_score)
        # print('epsilon program score', epsilon_program)
        # print('program score upper bound', program_current_score + epsilon_program)
        # print('program score upper bound (x500)', program_current_score + (epsilon_program * 500))
        # print('transform program score ub (100)', transform_program_curr_score + (epsilon_program * 100))
        # print('=' * 20)
        # print()

        if (program_current_score + epsilon_program) <= (self.best_eval - epsilon_current_best):
            return True

        return False