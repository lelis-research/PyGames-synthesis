"""
evaluation.py 

Author: Olivier Vadiavaloo

Description:
This module implements the evaluation object that will evaluate
generated programs through the is_correct method and by playing the
Catcher game implemented in 
https://pygame-learning-environment.readthedocs.io/en/latest/user/games/catcher.html

"""
import copy as cp
import pygame, time
from pygame.locals import *
from statistics import *

### import game from Pygame-Learning-Environment ###
from pygame_games.ple.games.catcher import Catcher
# from pygame_games.ple.games.pong import Pong
from pygame_games.ple.ple import PLE
from pong.pong3 import Pong
from src.evaluation_config import *

# keys: game
# values: number of players
available_games = {'Catcher': 1, 'Pong': 2}

class EvaluationFactory:

    def __init__(self, threshold, total_games, triage, batch):
        self.set_games_dict(threshold, total_games, triage, batch)

    def set_games_dict(self, threshold, total_games, triage, batch):
        self.games_dict = {
            'Catcher': EvaluationCatcher(threshold, total_games, triage, batch), 
            'Pong': EvaluationPong(threshold, total_games, triage, batch)
        }

    def get_eval_fun(self, eval_str):
        return self.games_dict[eval_str]

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
                try:
                    score = self.play(program)
                except:
                    self.clean_up()
                    return tuple([]), Evaluation.MIN_SCORE

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


class EvaluationPong(Evaluation):

    def __init__(self, score_threshold, total_games, triage, batch=True):
        super(EvaluationPong, self).__init__(score_threshold, total_games, triage, batch)

    def update_env(self, player, game_state, action_set):
        env = {}
        env['state'] = {}
        env['state']['non_player_position'] = game_state['ball_y']

        if player == 'p1':
            env['state']['non_player_approaching'] = game_state['ball_vel'] < 0
        else:
            env['state']['non_player_approaching'] = game_state['ball_vel'] > 0

        env['state']['player_position'] = game_state[player + '_pos']
        env['paddle_width'] = game_state['paddle_width']
        env['actions'] = action_set
        return env

    def get_score(self):
        return self.game.get_rewards()[0]   # return rewards of p1
    
    def init_game(self):
        self.game = Pong()

    def game_over(self):
        return (not self.game.continue_game or self.game.close_clicked)

    def play(self, program):
        actions = []
        p1 = program

        if self.best is not None:
            p2 = self.best
        else:
            p2 = cp.deepcopy(p1)

        env = self.update_env('p1', self.game.game_state(), [K_q, K_a, None])
        actions.append(p1.interpret(env))
        env = self.update_env('p2', self.game.game_state(), [K_p, K_l, None])
        actions.append(p2.interpret(env))

        self.game.step(actions)
        return self.get_score()


class EvaluationCatcher(Evaluation):


    def __init__(self, score_threshold, total_games, triage, batch=True):
        super(EvaluationCatcher, self).__init__(score_threshold, total_games, triage, batch)

    def set_batch(self, batch_eval_bool):
        previous_value = self.batch
        self.batch = batch_eval_bool
        return previous_value

    def update_env(self, game_state, action_set):
        """
        This method updates the env variable based on the game_state and
        the action set values.
        """
        env = {}
        env['state'] = {}
        env['state']['non_player_position'] = game_state.get('fruit_x')
        env['state']['non_player_approaching'] = True
        
        env['state']['player_position'] = game_state.get('player_x')
        env['paddle_width'] = game_state.get('paddle_width')
        env['actions'] = action_set
        return env

    def get_score(self):
        return self.game.getScore()

    def game_over(self):
        return self.game.game_over()

    def init_game(self):
        self.game = Catcher(width=500, height=500, init_lives=3)
        self.p = PLE(self.game, fps=30, display_screen=True, rng=int(time.time()))

    def play(self, program):
        env = self.update_env(self.p.getGameState(), self.p.getActionSet())
        action = program.interpret(env)
        self.p.act(action)
        return self.p.score()