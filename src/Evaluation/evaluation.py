"""
evaluation.py 

Author: Olivier Vadiavaloo

Description:
This module implements the evaluation factory that returns an instance of an evaluation
object that is used by the synthesizer to gauge the performance of generated programs.

See:
https://pygame-learning-environment.readthedocs.io/en/latest/user/games/catcher.html

"""
from src.Evaluation.evaluation_ple import *
from src.Evaluation.evaluation_pong import *
from src.Evaluation.evaluation_parent import *

# keys: game
# values: number of players
available_games = {'Catcher': 1, 'Pong': 2, 'FlappyBird': 1, 'Snake': 1}

class EvaluationFactory:

    def __init__(self, threshold, eval_config):
        self.games_dict = {
            'Catcher': EvaluationCatcher(threshold, eval_config), 
            'Pong': EvaluationPong(threshold, eval_config), 
            'FlappyBird': EvaluationFlappyBird(threshold, eval_config),
            'Snake': EvaluationSnake(threshold, eval_config)
        }

    def get_eval_fun(self, eval_str):
        return self.games_dict[eval_str]