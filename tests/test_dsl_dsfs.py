import unittest
from unittest.loader import makeSuite
from src.dsl import NonPlayerObjectPosition, PlayerPosition

class TestPlayerPosition(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['state'] = {}
        self.env['state']['player_position'] = 60

    def test_interpret_no_exception(self):
        p_position = PlayerPosition()
        self.assertEqual(p_position.interpret(self.env), 60, 'interpret method of PlayerPosition object should return 60')

    def test_interpret_key_error(self):
        p_position = PlayerPosition()
        self.env['state'].pop('player_position')
        test_msg = 'interpret method of PlayerPosition object should raise KeyError'

        with self.assertRaises(KeyError, msg=test_msg) as cm:
            p_position.interpret(self.env)

    def test_interpret_with_index(self):
        PlayerPosition.valid_children_types = [set([0, 1, 2])]
        p_position = PlayerPosition.new(2)
        self.env['state']['player_position'] = [60, 40, 100]
        self.assertEqual(p_position.interpret(self.env), 100, 'interpret method of PlayerPosition should return 100')


class TestNonPlayerPosition(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['state'] = {}
        self.env['state']['non_player_position'] = 55

    def test_interpret_no_exception(self):
        p_position = NonPlayerObjectPosition()
        self.assertEqual(p_position.interpret(self.env), 55, 'interpret method of NonPlayerObjectPosition object should return 60')

    def test_interpret_key_error(self):
        p_position = NonPlayerObjectPosition()
        self.env['state'].pop('non_player_position')
        test_msg = 'interpret method of NonPlayerObjectPosition object should raise KeyError'

        with self.assertRaises(KeyError, msg=test_msg) as cm:
            p_position.interpret(self.env)

    def test_interpret_with_index(self):
        NonPlayerObjectPosition.valid_children_types = [set([0, 1, 2])]
        p_position = NonPlayerObjectPosition.new(1)

        self.env['state']['non_player_position'] = [55, 45, 36]
        self.assertEqual(p_position.interpret(self.env), 45, 'interpret method NonPlayerObjectPosition object should return 45')


if __name__ == '__main__':
    unittest.main()