"""
Author: Olivier Vadiavaloo

Description:
This file contains the evaluation sub-class for the Pong domain.
"""
### import Pong game from pong3 ###
from pong.pong3 import *

from src.Evaluation.evaluation_parent import *
from pygame.locals import *
import copy as cp

class EvaluationPong(Evaluation):

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
        p1_score, p2_score = self.game.get_scores()
        if p1_score > p2_score:
            return 1
        else:
            return 0
    
    def init_game(self):
        self.game = Pong()

    def game_over(self):
        return (not self.game.continue_game or self.game.close_clicked)

    def play(self, program):
        actions = []
        p1 = program

        env = self.update_env('p1', self.game.game_state(), [K_q, K_a, None])
        action = p1.interpret(env)

        self.game.step(action)
        return self.get_score()