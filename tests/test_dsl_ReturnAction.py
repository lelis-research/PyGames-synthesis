import unittest
from src.dsl import *
from unittest.mock import Mock

class TestReturnAction(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['action'] = {}
        self.env['action']['LEFT'] = 5
        self.env['action']['RIGHT'] = 48

    def mockAction(self, value):
        action = Mock()
        action.getSize.return_value = 1
        action.interpret.return_value = self.env['action'][value]
        return action

    def test_size_two(self):
        # Test with action object of size 1
        # ret_action should return 1 + action.getSize() = 1 + 1 = 2
        action = self.mockAction('LEFT')
        ret_action = ReturnAction.new(action)
        self.assertEqual(ret_action.getSize(), 2, 'ReturnAction object should have size 2')
        
    def test_size_change_arg_size(self):
        # Manually change the mock action's size
        action = self.mockAction('LEFT')
        ret_action = ReturnAction.new(action)
        ret_action.get_children()[0].getSize.return_value = 100
        self.assertEqual(ret_action.getSize(), 2, 'ReturnAction object should have size 2')

    def test_size_change_action_size(self):
        # set action size to 1000
        # action.getSize should still return 5 because getSize was changed to lambda x : 5
        ret_action = ReturnAction.new(self.mockAction('LEFT'))
        ret_action.size = 1000
        self.assertEqual(ret_action.getSize(), 1000, 'ReturnAction object should size 1000')

    def test_interpret_left(self):
        # Test with action object with action string equal to 'LEFT'
        action = self.mockAction('LEFT')
        ret_action = ReturnAction.new(action)
        self.assertEqual(ret_action.interpret(self.env), 5, 'interpret method of ReturnAction object should return 5')

    def test_interpret_right(self):
        # Test with action object with action string equal to 'RIGHT'
        action = self.mockAction('RIGHT')
        ret_action = ReturnAction.new(action)
        self.assertEqual(ret_action.interpret(self.env), 48, 'interpret method of ReturnAction object should return 48')


if __name__ == '__main__':
    unittest.main()