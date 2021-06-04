import unittest
from unittest.mock import Mock
from src.dsl import IT, ReturnAction

class TestIT(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['TRUE'] = True
        self.env['FALSE'] = False
        self.env['BODY'] = 100  

        # Create mock object
        self.if_cond = Mock()
        self.if_body = Mock()
        
        type(self.if_body).__name__ = 'ReturnAction'

        self.if_cond.getSize.return_value = 1
        self.if_body.getSize.return_value = 1

    def init_IT(self, cond, body):
        self.if_cond.interpret.return_value = self.env[cond]
        self.if_body.interpret.return_value = self.env[body]
        return IT.new(self.if_cond, self.if_body)      

    def test_size_three(self):
        it = self.init_IT('TRUE', 'BODY')

        # cond and body both have size 1
        self.assertEqual(it.getSize(), 3, 'IT object should have size 3')
        
    def test_size_change_it_size(self):
        it = self.init_IT('TRUE', 'BODY')

        # Manually change it.size to 100
        it.size = 100
        self.assertEqual(it.getSize(), 100, 'IT object should have size 100')

    def test_size_change_arg_sizes(self):
        # Manually change cond.size and body.size,
        # and re-instantiate an IT object
        it = IT.new(self.if_cond, self.if_body)
        it.get_children()[0].getSize.return_value = 12
        it.get_children()[1].getSize.return_value = 3
        self.assertEqual(it.getSize(), 3, 'IT object should have size 3')

    def test_interpret_false_cond(self):
        # Test interpret method for if-condition evaluating to false
        it = self.init_IT('FALSE', 'BODY')
        self.assertEqual(it.interpret(self.env), None, 'interpret method of IT should return None')

    def test_interpret_true_cond(self):
        # Test interpret method for if-condition evaluating to True
        it = self.init_IT('TRUE', 'BODY')
        self.assertEqual(it.interpret(self.env), 100, 'interpret method of IT should return 100')

if __name__ == '__main__':
    unittest.main()