import unittest
from unittest.loader import makeSuite
from DSL import PlayerPosition, FallingFruitPosition

class TestPlayerPosition(unittest.TestCase):

    def init_env(self):
        self.env = {}
        self.env['state'] = {}
        self.env['state']['player_position'] = 60

    def test_interpret_no_exception(self):
        self.init_env()
        p_position = PlayerPosition()
        self.assertEqual(p_position.interpret(self.env), 60, 'interpret method of PlayerPosition object should return 60')

    def test_interpret_key_error(self):
        self.init_env()
        p_position = PlayerPosition()
        self.env['state'].pop('player_position')
        test_msg = 'interpret method of PlayerPosition object should raise KeyError'

        with self.assertRaises(KeyError, msg=test_msg) as cm:
            p_position.interpret(self.env)


class TestFallingFruitPosition(unittest.TestCase):

    def init_env(self):
        self.env = {}
        self.env['state'] = {}
        self.env['state']['fruit_position'] = 55

    def test_interpret_no_exception(self):
        self.init_env()
        p_position = FallingFruitPosition()
        self.assertEqual(p_position.interpret(self.env), 55, 'interpret method of FallingFruitPosition object should return 60')

    def test_interpret_key_error(self):
        self.init_env()
        p_position = FallingFruitPosition()
        self.env['state'].pop('fruit_position')
        test_msg = 'interpret method of FallingFruitPosition object should raise KeyError'

        with self.assertRaises(KeyError, msg=test_msg) as cm:
            p_position.interpret(self.env)


if __name__ == '__main__':
    unittest.main()