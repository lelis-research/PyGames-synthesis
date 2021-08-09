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
from pygame_games.ple import games
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
    by_win_rate_name = 'by_win_rate'

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

        # by_win_rate can be None by default
        self.by_win_rate = attributes.get(self.by_win_rate_name)
        if self.by_win_rate:
            self.triage_random_var_bound = 1

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

    def set_best_eval_variance(self, variance):
        pass

    def get_best_eval(self):
        return self.best_eval

    def get_random_var_bound(self):
        return self.triage_random_var_bound

    def get_confidence_value(self):
        return self.triage_confidence_value

    def clean_up(self):
        pass

    def compute_result(self, scores, games_played):
        raise Exception('Must implement compute_result')

    def compute_win_rate(self, wins_and_losses, games_played):
        # wins represented by 1's, losses represented by 0's
        filtered_win_scores = list(filter(lambda arg: arg == 1, wins_and_losses))
        num_wins = len(filtered_win_scores)
        return round(num_wins / games_played, 2)

    def check_continue(self, program_current_score, games_played):
        raise Exception('Must implement check_continue method')

    def compute_epsilon(self, number_evals):
        # Hoeffding inequality
        return self.triage_random_var_bound * \
            math.sqrt(math.log(2 / (1 - math.sqrt(self.triage_confidence_value))) / (2 * number_evals))

    def check_triage_stop(self, program_current_score, epsilon_program, epsilon_current_best):

        # epsilon_program = compute_epsilon(games_played_so_far)
        # epsilon_current_best = compute_epsilon(total_games_to_be_played)

        if (program_current_score + epsilon_program) <= (self.best_eval - epsilon_current_best):
            return True

        return False