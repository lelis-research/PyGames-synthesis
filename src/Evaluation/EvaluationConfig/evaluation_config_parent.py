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

class EvaluationConfig:

    total_games_name = 'total_games'
    best_eval_name = 'best_eval'
    min_score_name = 'MIN_SCORE'
    triage_name = 'triage'
    batch_size_name = 'batch_size'

    def __init__(self, attributes):
        self.config_attributes_set = False
        self.set_config_attributes(attributes)

    def set_config_attributes(self, attributes):
        self.triage = attributes[self.triage_name]
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

    def slack(self, games_played):
        slack_value = self.best_eval * (((self.total_games - games_played) * 1.75) / self.total_games)
        if slack_value < 0:
            slack_value *= -1

        return slack_value

    def clean_up(self):
        pass

    def compute_results(self, scores, games_played):
        raise Exception('Must implement compute_results method')

    def check_continue(self, games_played):
        raise Exception('Must implement check_continue method')

    def check_triage_stop(self, games_played):
        raise Exception('Must implement check_triage_stop')