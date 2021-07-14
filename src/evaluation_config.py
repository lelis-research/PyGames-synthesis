"""
evaluation_config.py

Author: Olivier Vadiavaloo
"""
from statistics import *

class EvaluationConfigFactory:

    def __init__(self, batch, triage):
        self.batch = batch
        self.triage = triage

    def get_config(self):
        if self.batch:
            return EvaluationConfigBatch(self.triage)
        
        else:
            return EvaluationConfigNormal(self.triage)


class EvaluationConfigBatch:

    def __init__(self, triage):
        self.triage = triage
        self.config_attributes_set = False

    def set_config_attributes(self, batch_size, total_games, best_eval):
        self.batch_size = batch_size
        self.total_games = total_games
        self.best_eval = best_eval
        self.clean_up()

    def set_min_score(self, min_score):
        self.MIN_SCORE = min_score

    def clean_up(self):
        self.max_scores = []
        self.last_score_index = 0

    def compute_result(self, scores, games_played):
        if not self.config_attributes_set:
            raise Exception(
                'Must set attributes of EvaluationConfigBatch object using set_config_attributes'
            )

        if games_played % self.batch_size == 0:
            batch_scores = scores[self.last_score_index:]
            max_batch_score = max(batch_scores)
            self.max_scores.append(max_batch_score)
            self.last_score_index = len(scores)

        if len(self.max_scores) > 0:
            return round(mean(self.max_scores), 2)
        else:
            return self.MIN_SCORE

    def check_triage_stop(self, games_played):
        # Check if mean score is less than best score 
        # and number of batches is equal to batch size
        num_batches = games_played // self.batch_size
        return mean(self.max_scores) < self.best_eval and num_batches >= self.batch_size

    def check_continue(self, games_played):
        if games_played == self.total_games:
            self.last_score_index = 0
            return False

        if self.triage:
            if len(self.max_scores) > 0 and self.check_triage_stop(games_played):
                self.last_score_index = 0
                return False

        return True

class EvaluationConfigNormal:

    def __init__(self, triage):
        self.triage = triage
        self.config_attributes_set = False

    def set_config_attributes(self, total_games, best_eval):
        self.total_games = total_games
        self.best_eval = best_eval

    def clean_up(self):
        pass

    def check_triage_stop(self, games_played):
        return self.average_score < self.best_eval \
            and games_played >= 0.5 * self.total_games

    def clean_up(self):
        pass

    def check_continue(self, games_played):
        if games_played == self.total_games:
            return False

        if self.triage and self.check_triage_stop(games_played):
            return False

        return True

    def compute_result(self, scores, games_played):
        self.average_score = round(mean(scores), 2)
        return self.average_score