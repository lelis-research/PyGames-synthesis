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
available_games = {'Catcher': 1, 'Pong': 2, 'FlappyBird': 1}

class EvaluationFactory:

    def __init__(self, threshold, total_games, triage, batch):
        self.set_games_dict(threshold, total_games, triage, batch)

    def set_games_dict(self, threshold, total_games, triage, batch):
        self.games_dict = {
            'Catcher': EvaluationCatcher(threshold, total_games, triage, batch), 
            'Pong': EvaluationPong(threshold, total_games, triage, batch), 
            'FlappyBird': EvaluationFlappyBird(threshold, total_games, triage, batch)
        }

    def get_eval_fun(self, eval_str):
        return self.games_dict[eval_str]