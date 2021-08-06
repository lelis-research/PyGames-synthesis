"""
evaluation_config.py

Author: Olivier Vadiavaloo

Description:
This file implements the classes used by synthesizers to evaluate
generated programs. A factory object is used to obtain an Evaluation
object based on desired configuration (triage, batch).
"""
from src.Evaluation.EvaluationConfig.evaluation_config_cheby import EvaluationConfigCheby
from statistics import *
from src.Evaluation.EvaluationConfig.evaluation_config_normal import *
from src.Evaluation.EvaluationConfig.evaluation_config_batch import *

class EvaluationConfigFactory:

    def get_config(self, config_name, config_attributes):
        if config_name == 'BATCH':
            return EvaluationConfigBatch(config_attributes)
        
        elif config_name == 'NORMAL':
            return EvaluationConfigNormal(config_attributes)

        elif config_name == 'CHEBY':
            return EvaluationConfigCheby(config_attributes)

        else:
            raise Exception(f'No such EvaluationConfig object: {self.config_name}')


def form_basic_attr_dict(
        triage, 
        var_bound, 
        confidence_value, 
        total_games, 
        best_eval, 
        min_score, 
        batch_size
    ):
    config_attributes = {}

    config_attributes[EvaluationConfig.triage_name] = triage
    config_attributes[EvaluationConfig.triage_var_bound_name] = var_bound
    config_attributes[EvaluationConfig.confidence_value_name] = confidence_value

    config_attributes[EvaluationConfig.best_eval_name] = best_eval
    config_attributes[EvaluationConfig.total_games_name] = total_games
    config_attributes[EvaluationConfig.min_score_name] = min_score
    config_attributes[EvaluationConfig.batch_size_name] = batch_size

    return config_attributes