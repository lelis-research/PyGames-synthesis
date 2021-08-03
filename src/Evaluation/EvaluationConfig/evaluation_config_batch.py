"""
evaluation_config_batch.py

Author: Olivier Vadiavaloo

Description:
This file implements an EvaluationConfig sub-class. In contrast to EvaluationConfigNormal,
this class keeps track of the maximum scores of batches of games played by the strategy provided
by the synthesizer and returns the average of the maximum scores as the strategy's score.
"""

from src.Evaluation.EvaluationConfig.evaluation_config_parent import *
from statistics import *

class EvaluationConfigBatch(EvaluationConfig):
    
    def set_config_attributes(self, attributes):
        self.batch_size = attributes[self.batch_size_name]
        assert type(self.batch_size) is int, 'batch_size must be an integer'

        super(EvaluationConfigBatch, self).set_config_attributes(attributes)

    def set_batch_size(self, batch_size):
        old_value = batch_size
        self.batch_size = batch_size
        return old_value

    def get_batch_size(self):
        return self.batch_size

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

    def check_continue(self, program_current_score, games_played):
        if games_played == self.total_games:
            self.last_score_index = 0
            return False

        if self.triage and len(self.max_scores) > 0:
            if self.check_triage_stop(program_current_score, games_played):
                self.last_score_index = 0
                return False

        return True