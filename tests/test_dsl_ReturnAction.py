import unittest
from DSL import *

class TestReturnAction(unittest.TestCase):

    class Action:

        def __init__(self, action):
            self.size = 1
            self.action = action

        def getSize(self):
            return self.size

        def interpret(self, env):
            return env['action'][self.action]

    def init_env(self):
        self.env = {}
        self.env['action'] = {}
        self.env['action']['LEFT'] = 5
        self.env['action']['RIGHT'] = 48

    def test_size(self):
        # Test with action object of size 1
        # ret_action should return 1 + action.getSize() = 1 + 1 = 2
        action = TestReturnAction.Action('LEFT')
        ret_action = ReturnAction(action)
        self.assertEqual(ret_action.getSize(), 2, '#1 ReturnAction object should have size 2')
        
        # Test action object with modified getSize method
        # action.getSize method always returns a size of 5 regardless of self.size's value
        TestReturnAction.Action.getSize = lambda x : 5
        action = TestReturnAction.Action('LEFT')
        ret_action = ReturnAction(action)
        self.assertEqual(ret_action.getSize(), 6, '#2 ReturnAction object should have size 6')

        # set action size to 1000
        # action.getSize should still return 5 because getSize was changed to lambda x : 5
        action.size = 1000
        self.assertEqual(ret_action.getSize(), 6, '#3 ReturnAction object should size 6')

    def test_interpret(self):
        # Test with action object with action string equal to 'LEFT'
        self.init_env()
        action = TestReturnAction.Action('LEFT')
        ret_action = ReturnAction(action)
        self.assertEqual(ret_action.interpret(self.env), 5, '#1 interpret method of ReturnAction object should return 5')

        # Test with action object with action string equal to 'RIGHT'
        action = TestReturnAction.Action('RIGHT')
        ret_action = ReturnAction(action)
        self.assertEqual(ret_action.interpret(self.env), 48, '#2 interpret method of ReturnAction object should return 48')


if __name__ == '__main__':
    unittest.main()