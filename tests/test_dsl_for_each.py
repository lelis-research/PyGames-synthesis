import unittest
from unittest import mock
from src.dsl import ForEach, IT, VarArray
from unittest.mock import Mock

class TestForEach(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['action'] = [191, 83, None]

        self.mock_iterable = Mock()
        self.mock_iterable.__class__ = VarArray
        self.mock_iterable.size = 1
        self.mock_iterable.get_size.return_value = 1
        self.mock_iterable.interpret.return_value = [191, 83, None]

        self.mock_loop_body = Mock()
        self.mock_loop_body.__class__ = IT
        self.mock_loop_body.size = 1
        self.mock_loop_body.get_size.return_value = 1
    
    def test_size_three(self):
        for_each = ForEach.new(self.mock_iterable, self.mock_loop_body)
        self.assertEqual(for_each.get_size(), 3, 'ForEach object should have size 3')

    def test_size_change_size(self):
        for_each = ForEach.new(self.mock_iterable, self.mock_loop_body)
        for_each.size = 100
        self.assertEqual(for_each.get_size(), 100, 'ForEach object should have size 100')

    def test_interpret(self):
        def mock_interpret(env):
            if env['loop'] == 83:
                return 83
            return 'False'

        self.mock_loop_body.interpret.side_effect = mock_interpret
        for_each = ForEach.new(self.mock_iterable, self.mock_loop_body)
        self.assertEqual(for_each.interpret(self.env), 83, 'ForEach.interpret should return 83')        


if __name__ == '__main__':
    unittest.main()