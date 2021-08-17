"""
evaluation_ple.py

Author: Olivier Vadiavaloo

Description:
This file contains the implementation of the evaluation sub-classes for PLE games.
"""
### import games from Pygame-Learning-Environment ###
from pygame_games.ple.games.catcher import Catcher
from pygame_games.ple.games.pong import Pong
from pygame_games.ple.games.flappybird import FlappyBird
from pygame_games.ple.games.snake import Snake
from pygame_games.ple.ple import PLE

from src.Evaluation.evaluation_parent import *

import time
import random

class EvaluationPle(Evaluation):

    def get_score(self):
        return self.game.getScore()

    def game_over(self):
        return self.game.game_over()

    def play(self, program):
        env = self.update_env(self.p.getGameState(), self.p.getActionSet())
        action = program.interpret(env)
        self.p.act(action)
        return self.p.score()

    def clean_up(self):
        self.game = None
        self.p = None
        super(EvaluationPle, self).clean_up()


class EvaluationCatcher(EvaluationPle):

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

    def init_game(self):
        self.game = Catcher(width=500, height=500, init_lives=3)
        self.p = PLE(self.game, fps=30, display_screen=False, rng=int(time.time()))


class EvaluationPong(EvaluationPle):

    def update_env(self, game_state, action_set):
        env = {}
        env['state'] = {}
        env['state']['non_player_approaching'] = game_state['ball_velocity_x'] < 0
        env['state']['non_player_position'] = game_state['ball_y']
        env['state']['player_position'] = game_state['player_y']

        env['paddle_width'] = game_state.get('paddle_width')
        env['actions'] = action_set
        return env

    def init_game(self):
        self.game = Pong(width=500, height=500, MAX_SCORE=20)
        self.p = PLE(self.game, fps=30, display_screen=True, rng=int(time.time()))


class EvaluationFlappyBird(EvaluationPle):

    STRONG_SCORE = 55

    def update_env(self, game_state, action_set):
        """
        This method updates the env variable based on the game_state and
        the action set values.
        """
        env = {}
        env['state'] = {}
        env['state']['non_player_approaching'] = True
        env['state']['non_player_dist_to_player'] = game_state.get('next_pipe_dist_to_player')
        env['state']['non_player_position'] = []
        env['state']['non_player_position'].append(game_state.get('next_pipe_top_y'))
        env['state']['non_player_position'].append(game_state.get('next_pipe_bottom_y'))

        env['state']['player_position'] = game_state.get('player_y')
        env['state']['player_velocity'] = game_state.get('player_vel')
        env['paddle_width'] = game_state.get('paddle_width')
        env['actions'] = action_set

        return env

    def init_game(self):
        self.game = FlappyBird()
        self.p = PLE(self.game, fps=30, display_screen=False, rng=random.choice([2, 3, 5, 7, 11, 91]))


class EvaluationSnake(EvaluationPle):

    def update_env(self, game_state, action_set):
        env = {}
        env['state'] = {}
        env['state']['non_player_approaching'] = True
        env['state']['non_player_position'] = []
        env['state']['non_player_position'].append(game_state.get('food_x'))
        env['state']['non_player_position'].append(game_state.get('food_y'))
        
        env['state']['player_position'] = []
        env['state']['player_position'].append(game_state.get('snake_head_x'))
        env['state']['player_position'].append(game_state.get('snake_head_y'))
        
        env['state']['player_direction'] = []
        env['state']['player_direction'].append(game_state.get('snake_dir').x)
        env['state']['player_direction'].append(game_state.get('snake_dir').y)

        env['paddle_width'] = game_state.get('paddle_width')
        env['body_dist_list'] = game_state['snake_body']
        env['actions'] = action_set

    def init_game(self):
        self.game = Snake()
        self.p = PLE(self.game, fps=30, display_screen=False, rng=int(time.time()))