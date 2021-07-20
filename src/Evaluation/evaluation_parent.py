"""
evaluation_parent.py

Author: Olivier Vadiavaloo

Description:
This file implements the parent Evaluation class.
"""
from src.Evaluation.evaluation_config import *
from statistics import *

class Evaluation:

    MIN_SCORE = -1_000_000
    STRONG_SCORE = 500

    def __init__(self, score_threshold, total_games, triage, batch):
        self.score_threshold = score_threshold
        self.total_games = total_games
        self.best = None
        self.best_eval = Evaluation.MIN_SCORE
        self.batch_size = 5

        config_factory = EvaluationConfigFactory(batch, triage)
        self.eval_config = config_factory.get_config()

        if batch:
            self.eval_config.set_config_attributes(self.batch_size, self.total_games, self.best_eval, Evaluation.MIN_SCORE)
        else:
            self.eval_config.set_config_attributes(total_games, self.best_eval)

    def set_total_games(self, new_total_games):
        previous_total_games = self.total_games
        self.total_games = new_total_games
        return previous_total_games

    def set_config(self, eval_config):
        self.eval_config = eval_config
    
    def change_config(self, batch, triage, batch_size=None):
        previous_eval_config = self.eval_config
        config_factory = EvaluationConfigFactory(batch, triage)
        self.eval_config = config_factory.get_config()

        if batch:
            assert batch_size is not None
            self.eval_config.set_config_attributes(batch_size, self.total_games, self.best_eval)
        else:
            self.eval_config.set_config_attributes(self.total_games, self.best_eval)

        return previous_eval_config

    def set_best(self, best, best_eval):
        self.best = best
        self.best_eval = best_eval
    
    def get_best(self):
        return self.best, self.best_eval

    def get_score(self):
        raise Exception('Must implement get_score method')

    def game_over(self):
        raise Exception('Must implement game_over method')

    def play(self):
        raise Exception('Must implement play method')

    def update_env(self):
        raise Exception('Must implement update_env method')
    
    def init_game(self):
        raise Exception('Must implement init_game method')

    def slack(self, games_played):
        return 0
    
    def clean_up(self):
        self.eval_config.clean_up()

    def compute_result(self, scores, games_played):
        return self.eval_config.compute_result(scores, games_played)

    def check_continue(self, games_played):
        return self.eval_config.check_continue(games_played)

    def evaluate(self, program, verbose=False):
        """
        The evaluate method runs a game and uses the program parameter as
        strategy to determine which actions to take at each game tick. It then
        returns the score of the program when the game is over or when an exception
        is raised due to an impossible action.
        """
        scores = []
        score = Evaluation.MIN_SCORE
        games_played = 0
        continue_eval = True
        while continue_eval:
            self.init_game()
            while not self.game_over():
                # try:
                score = self.play(program)
                # except:
                #     self.clean_up()
                #     return tuple([]), Evaluation.MIN_SCORE

            games_played += 1
            scores.append(score)

            result = self.compute_result(scores, games_played)
            continue_eval = self.check_continue(games_played)

        self.clean_up()
        if verbose:
            return tuple(scores), result
        else:
            return result

    def is_correct(self, program):
        """
        The evaluate method runs a game and uses the program parameter as
        strategy to determine which actions to take at each game tick. It then
        returns the score of the program when the game is over or when an exception
        is raised due to an impossible action.
        """
        score = self.evaluate(program)
        
        if score < self.score_threshold:
            return False, score
        else:
            self.score_threshold = score
            return True, score
