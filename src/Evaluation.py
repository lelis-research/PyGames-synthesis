"""
Evaluation.py 

Author: Olivier Vadiavaloo

Description:
This module implements the evaluation object that will evaluate
generated programs through the is_correct method and by playing the
Catcher game implemented in 
https://pygame-learning-environment.readthedocs.io/en/latest/user/games/catcher.html

"""
### import game from Pygame-Learning-Environment ###

class Evaluation:

    def __init__(self, threshold):
        self.score_threshold = threshold

    def update_env(game_state, action_set):
        """
        This method updates the env variable based on the game_state and
        the action set values.
        """
        env = {}
        env['state']['fruit_x'] = game_state['fruit_x']
        env['state']['player_position'] = game_state['player_x']
        env['paddle_width'] = game_state['paddle_width']
        env['actions'] = action_set
        return env

    def is_correct(self, program):
        """
        The is_correct method evaluates a generated program passed in as parameter.
        This method basically initializes a Catcher game and every time an action is
        required by the game, the synthesized program's interpret method is called
        and the returned action is passed on to the act method of the PLE object.
        """
        game = Catcher(width=500, height=500, init_lives=3)
        p = PLE(game, fps=30, display_screen=False)

        while not p.game_over():
            env = self.update_env(p.getGameState(), p.getActionSet())
            try:
                action = program.interpret(env)
            except:
                return False, 0
            p.act(action)
        
        if p.score() < self.score_threshold:
            return False, p.score()
        else:
            return True, p.score()
