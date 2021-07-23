"""
evaluation_config_normal.py

Author: Olivier Vadiavaloo

Description:
This file implements an EvaluationConfig sub-class. It is called EvaluationConfigNormal
because in contrast to EvaluationConfigBatch, it simply computes the mean of all the scores
it receives. As every EvaluationConfig sub-class, it can run with a triage option and the 
check to stop the triage evaluation is implemented by the sub-class itself.
"""
from src.Evaluation.EvaluationConfig.evaluation_config_parent import *
from statistics import *

class EvaluationConfigNormal(EvaluationConfig):

    def check_triage_stop(self, games_played):
        return self.average_score < self.best_eval - self.slack(games_played) \
            and games_played >= 0.5 * self.total_games

    def check_continue(self, games_played):
        if games_played == self.total_games:
            return False

        if self.triage and self.check_triage_stop(games_played):
            return False

        return True

    def compute_result(self, scores, games_played):
        if not self.config_attributes_set:
            raise Exception(
                'Must set attributes of EvaluationConfigBatch object using set_config_attributes'
            )
        
        self.average_score = round(mean(scores), 2)
        return self.average_score