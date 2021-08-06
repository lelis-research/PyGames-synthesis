"""
"""

from src.Evaluation.EvaluationConfig.evaluation_config_parent import *
import math

class EvaluationConfigCheby(EvaluationConfig):

    k_eval_name = 'k_eval'

    def set_config_attributes(self, attributes):
        self.k_eval = attributes.get(self.k_eval_name)
        if self.k_eval is None:
            self.k_eval = 10
            
        assert type(self.k_eval) is int, 'k_eval must be an integer'

        self.best_eval_variance = 0

        return super().set_config_attributes(attributes)

    def set_k_eval(self, k_eval):
        old_value = self.k_eval
        self.k_eval = k_eval
        return old_value

    def set_best_eval_variance(self, variance):
        self.best_eval_variance = variance

    def clean_up(self):
        self.can_check_triage = False

    def compute_result(self, scores, games_played):
        self.scores = scores

        if games_played == self.k_eval:
            self.variance = variance(scores)

        if games_played % self.k_eval == 0:
            self.can_check_triage = True
        else:
            self.can_check_triage = False
            
        if self.by_win_rate:
            return self.compute_win_rate(scores, games_played)

        return round(mean(scores), 2)

    def check_continue(self, program_current_score, games_played):
        if games_played == self.total_games:
            return False

        if self.triage and self.can_check_triage:
            if self.check_triage_stop(
                    program_current_score,
                    self.compute_epsilon(self.variance, games_played),
                    self.compute_epsilon(self.best_eval_variance, self.total_games)
            ):
                return False

        return True

    def compute_epsilon(self, variance, number_evals):
        # Chebyshev inequality
        return math.sqrt(variance / (self.triage_confidence_value * number_evals))