import unittest
from DSL import *

class TestOwnStrategy(unittest.TestCase):

    def init_attributes(self):
        self.env = {}
        self.env['state'] = {}
        self.env['action'] = ['LEFT', 'RIGHT', None]
        self.create_strategy()

    def create_strategy(self):
        """
        My strategy for playing Catcher is the following:
            
            if FallingFruitPosition > PlayerPosition + (paddle_width // 2):
                return action[1]
            if FallingFruitPosition < PlayerPosition - (paddle_width // 2):
                return action[0]
        """
        self.str_representation = "if FallingFruitPosition > (PlayerPosition + (paddle_width // 2)):\n\t"
        self.str_representation += "return action[1]\n"
        self.str_representation += "if FallingFruitPosition < (PlayerPosition - (paddle_width // 2)):\n\t"
        self.str_representation += "return action[0]\n"
        self.str_representation += "return action[2]"
        self.program = Strategy(
            IT( 
                GreaterThan( FallingFruitPosition(), Plus( PlayerPosition(), Divide( VarScalar('paddle_width'), Constant(2) ) ) ),
                    ReturnAction( VarFromArray('action', Constant(1)) )
            ),
            Strategy( 
                IT( 
                    LessThan( FallingFruitPosition(), Minus( PlayerPosition(), Divide( VarScalar('paddle_width'), Constant(2) ) ) ), 
                        ReturnAction( VarFromArray('action', Constant(0)) )
                ),
                ReturnAction( VarFromArray('action', Constant(2)) )
            ),
        )

    def test_to_string(self):
        self.init_attributes()
        print('\n' + self.program.toString())
        self.assertEqual(self.program.toString(), self.str_representation, "Invalid string representation")

    def test_action_right(self):
        self.init_attributes()
        self.env['paddle_width'] = 100
        self.env['state']['player_position'] = 35
        self.env['state']['fruit_position'] = 100

        """
        (1) player_position + (paddle_width // 2) = 35 + (100 // 2) = 85
        (2) fruit_position = 100
        Hence, (2) > (1). First if-statement evaluates to True.
        The program should return actions[1] (which is 'RIGHT') on interpretation.
        """
        self.assertEqual(self.program.interpret(self.env), 'RIGHT', "Should return 'RIGHT'")

    def test_action_left(self):
        self.init_attributes()
        self.env['paddle_width'] = 100
        self.env['state']['player_position'] = 100
        self.env['state']['fruit_position'] = 35

        """
        (1) player_position - (paddle_width // 2) = 100 - (100 // 2) = 50
        (2) fruit_position = 35
        Hence, (2) < (1). First if-statement evaluates to False.
        The program should return actions[0] (which is 'LEFT') on interpretation.
        """
        self.assertEqual(self.program.interpret(self.env), 'LEFT', "Should return 'LEFT'")

    def test_action_none(self):
        self.init_attributes()
        self.env['paddle_width'] = 100
        self.env['state']['player_position'] = 50
        self.env['state']['fruit_position'] = 50

        """
        (1) player_position - (paddle_width // 2) = 50 - (100 // 2) = 0
        (2) player_position + (paddle_width // 2) = 50 + (100 // 2) = 100
        (3) fruit_position = 50
        Hence, (3) > (1) and (3) < (2). Both if-statements evaluate to False.
        The program should return actions[2] (which is None) on interpretation.
        """
        self.assertEqual(type(self.program.interpret(self.env)).__name__, type(None).__name__, "Should return None")


if __name__ == '__main__':
    unittest.main()
