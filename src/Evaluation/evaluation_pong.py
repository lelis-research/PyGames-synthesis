"""
Author: Olivier Vadiavaloo

Description:
This file
"""
### import Pong game from pong3 ###
from pong.pong3 import *

from src.Evaluation.evaluation_parent import *
from pygame.locals import *
import copy as cp

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