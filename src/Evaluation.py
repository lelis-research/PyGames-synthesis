"""
evaluation.py 

Author: Olivier Vadiavaloo

Description:
This module implements the evaluation object that will evaluate
generated programs through the is_correct method and by playing the
Catcher game implemented in 
https://pygame-learning-environment.readthedocs.io/en/latest/user/games/catcher.html

"""
### import game from Pygame-Learning-Environment ###
from pygame_games.ple.games.catcher import Catcher
from pygame_games.ple.ple import PLE

class Evaluation:

    def __init__(self, threshold):
        self.score_threshold = threshold

    def update_env(self, game_state, action_set):
        """
        This method updates the env variable based on the game_state and
        the action set values.
        """
        env = {}
        env['state'] = {}
        env['state']['fruit_position'] = game_state['fruit_x']
        env['state']['player_position'] = game_state['player_x']
        env['paddle_width'] = game_state['paddle_width']
        env['actions'] = action_set
        return env

    def evaluate(self, program):
        """
        The evaluate method runs a Catcher game and uses the program parameter as
        strategy to determine which actions to take at each game tick. It then
        returns the score of the program when the game is over or when an exception
        is raised due to an impossible action.
        """
        game = Catcher(width=500, height=500, init_lives=3)
        p = PLE(game, fps=30, display_screen=False)

        score = -100000
        while not p.game_over():
            env = self.update_env(p.getGameState(), p.getActionSet())
            try:
                action = program.interpret(env)
            except:
                return 0
            p.act(action)
            score = p.score()

        return score

    def is_correct(self, program):
        """
        This method calls the evaluate method which returns the score of the program
        in a Catcher game. It then uses the score to determine if the program is
        'correct', that is if the latter's score is greater than or equal to the
        self.score_threshold attribute. If yes, it returns True and the score of the
        program. Otherwise, it returns False and the score.
        """
        score = self.evaluate(program)
        
        if score < self.score_threshold:
            return False, score
        else:
            self.score_threshold = score
            return True, score