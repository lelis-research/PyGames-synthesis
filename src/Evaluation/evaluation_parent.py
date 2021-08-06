"""
evaluation_parent.py

Author: Olivier Vadiavaloo

Description:
This file implements the parent Evaluation class.
"""
from src.Evaluation.EvaluationConfig.evaluation_config import *
from statistics import *
from functools import partial
from concurrent.futures import ProcessPoolExecutor
import os

class Evaluation:

    MIN_SCORE = -1_000_000
    STRONG_SCORE = 100

    def __init__(self, score_threshold, eval_config):
        self.score_threshold = score_threshold
        self.best = None
        self.eval_config = eval_config

    def set_total_games(self, new_total_games):
        return self.eval_config.set_total_games(new_total_games)

    def get_total_games(self):
        return self.eval_config.get_total_games()

    def set_config(self, eval_config):
        self.eval_config = eval_config
    
    def change_config(self, config_name, config_attributes):
        old_eval_config = self.eval_config
        config_factory = EvaluationConfigFactory()
        self.eval_config = config_factory.get_config(config_name, config_attributes)

        return old_eval_config

    def set_best(self, best, best_eval, scores):
        self.best = best
        self.eval_config.set_best_eval(best_eval)
        
        if best_eval == self.MIN_SCORE:
            self.eval_config.set_best_eval_variance(0)
        else:
            self.eval_config.set_best_eval_variance(variance(scores))
    
    def get_best(self):
        return self.best, self.eval_config.get_best_eval()

    def get_score(self):
        raise Exception('Must implement get_score method')

    def get_confidence_value(self):
        return self.eval_config.get_confidence_value()

    def get_random_var_bound(self):
        return self.eval_config.get_random_var_bound()

    def game_over(self):
        raise Exception('Must implement game_over method')

    def play(self):
        raise Exception('Must implement play method')

    def update_env(self):
        raise Exception('Must implement update_env method')
    
    def init_game(self):
        raise Exception('Must implement init_game method')
    
    def clean_up(self):
        self.eval_config.clean_up()

    def compute_result(self, scores, games_played):
        return self.eval_config.compute_result(scores, games_played)

    def check_continue(self, current_program_score, games_played):
        return self.eval_config.check_continue(current_program_score, games_played)

    def evaluate_parallel(self, program, verbose=False):
        """
        This method runs a game and uses the program parameter as the strategy 
        to determine which actions to take at each game step. It works just like 
        the evaluate() method, except it executes the games in parallel. This can 
        speed up the evaluation phase if total_games is larger (e.g 1000).
        """
        old_total_games = self.eval_config.get_total_games()

        new_config_attributes = form_basic_attr_dict(
                                    False,
                                    None,
                                    None,
                                    1,
                                    self.get_best()[1],
                                    Evaluation.MIN_SCORE,
                                    None
                                )

        old_eval_config = self.change_config('NORMAL', new_config_attributes)

        cpu_count = int(os.environ.get('SLURM_JOB_CPUS_PER_NODE', default=os.cpu_count()))

        scores = []
        with ProcessPoolExecutor(cpu_count) as executor:
            evaluate_args_list = [program for _ in range(old_total_games)]
            partial_evaluate = partial(self.evaluate, verbose=False)

            for res in executor.map(partial_evaluate, evaluate_args_list):
                scores.append(res)

        self.set_total_games(old_total_games)
        result = self.compute_result(scores, old_total_games)

        self.set_config(old_eval_config)

        if verbose:
            return scores, result
        else:
            return result

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
                try:
                    score = self.play(program)
                except:
                    self.clean_up()
                    return tuple([]), Evaluation.MIN_SCORE

            games_played += 1
            scores.append(score)

            result = self.compute_result(scores, games_played)
            continue_eval = self.check_continue(result, games_played)

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
