import unittest
from src.dsl import ITE, ReturnAction
from unittest.mock import Mock

class TestITE(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['TRUE'] = True
        self.env['FALSE'] = False
        self.env['IF_BODY'] = 100
        self.env['ELSE_BODY'] = 53
        
        self.if_cond = Mock()
        self.if_body = Mock()
        self.else_body = Mock()

        type(self.if_body).__name__ = 'ReturnAction'
        type(self.else_body).__name__ = 'ReturnAction'

        self.if_cond.getSize.return_value = 1
        self.if_body.getSize.return_value = 1
        self.else_body.getSize.return_value = 1

    def init_ITE(self, if_cond, if_body, else_body):
        self.if_cond.interpret.return_value = self.env[if_cond]
        self.if_body.interpret.return_value = self.env[if_body]
        self.else_body.interpret.return_value = self.env[else_body]
        return ITE.new(self.if_cond, self.if_body, self.else_body)

    def test_size_four(self):
        ite = self.init_ITE('TRUE', 'IF_BODY', 'ELSE_BODY')
        self.assertEqual(ite.getSize(), 4, 'ITE object should have size 4')

    def test_size_change_it_size(self):
        ite = self.init_ITE('TRUE', 'IF_BODY', 'ELSE_BODY')

        # Manually change the size of the ite instance
        ite.size = 100
        self.assertEqual(ite.getSize(), 100, 'ITE object should have size 100')

    def test_size_change_arg_size(self):
        # Manually change the size of the arguments to the ITE constructor
        ite = ITE.new(self.if_cond, self.if_body, self.else_body)
        ite.get_children()[0].getSize.return_value = 10
        ite.get_children()[1].getSize.return_value = 10
        ite.get_children()[2].getSize.return_value = 10
        self.assertEqual(ite.getSize(), 4, 'ITE object should have size 4')

    def test_interpret_false(self):
        # Test the interpret method with the if-condition evaluating to False
        ite = self.init_ITE('FALSE', 'IF_BODY', 'ELSE_BODY')
        self.assertEqual(ite.interpret(self.env), 53, 'interpret method of ITE object should return 53')

    def test_interpret_true(self):
        # Test the interpret method with the if-condition evaluating to True
        ite = self.init_ITE('TRUE', 'IF_BODY', 'ELSE_BODY')
        self.assertEqual(ite.interpret(self.env), 100, 'interpret method of ITE object should return 100')


if __name__ == '__main__':
    unittest.main()