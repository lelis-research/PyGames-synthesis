import unittest
from src.DSL import *

class TestOwnStrategy(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['state'] = {}
        self.env['action'] = ['LEFT', 'RIGHT', None]
        self.create_strategy()

    def create_strategy(self):
        """
        My strategy for playing Catcher is the following:
            
            if FallingFruitPosition > PlayerPosition + (paddle_width * 0.5):
                return action[1]
            if FallingFruitPosition < PlayerPosition - (paddle_width * 0.5):
                return action[0]
        """
        self.str_representation = "if FallingFruitPosition > (PlayerPosition + (paddle_width * 0.5)):\n\t"
        self.str_representation += "return action[1]\n"
        self.str_representation += "if FallingFruitPosition < (PlayerPosition - (paddle_width * 0.5)):\n\t"
        self.str_representation += "return action[0]\n"
        self.str_representation += "return action[2]"
        self.program = Strategy.new(
            IT.new( 
                GreaterThan.new( FallingFruitPosition(), Plus.new( PlayerPosition(), Times.new( VarScalar.new('paddle_width'), Constant.new(0.5) ) ) ),
                    ReturnAction.new( VarFromArray.new('action', Constant.new(1)) )
            ),
            Strategy.new( 
                IT.new( 
                    LessThan.new( FallingFruitPosition(), Minus.new( PlayerPosition(), Times.new( VarScalar.new('paddle_width'), Constant.new(0.5) ) ) ), 
                        ReturnAction.new( VarFromArray.new('action', Constant.new(0)) )
                ),
                ReturnAction.new( VarFromArray.new('action', Constant.new(2)) )
            ),
        )

    def test_to_string(self):
        print('\n' + self.program.toString())
        self.assertEqual(self.program.toString(), self.str_representation, "Invalid string representation")

    def test_action_right(self):
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
