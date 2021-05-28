import unittest
from DSL import IT, ReturnAction

class TestIT(unittest.TestCase):

    class IF_COND:

        def __init__(self, cond):
            self.size = 1
            self.cond = cond

        def getSize(self):
            return self.size

        def interpret(self, env):
            return env[self.cond]

    class IF_BODY:

        def __init__(self, body):
            self.size = 1
            self.body = body
            self.__class__.__name__ = 'ReturnAction'

        def getSize(self):
            return self.size

        def interpret(self, env):
            return env[self.body]

    def init_env(self):
        self.env = {}
        self.env['TRUE'] = True
        self.env['FALSE'] = False
        self.env['BODY'] = 100  

    def init_IT(self, cond, body):
        return IT(TestIT.IF_COND(cond), TestIT.IF_BODY(body))      

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
        cond = TestIT.IF_COND('TRUE')
        body = TestIT.IF_BODY('BODY')

        # Manually change cond.size and body.size,
        # and re-instantiate an IT object
        cond.size = 13
        body.size = 2
        it = IT(cond, body)
        self.assertEqual(it.getSize(), 16, 'IT object should have size 16')

    def test_interpret_false_cond(self):
        # Test interpret method for if-condition evaluating to false
        self.init_env()
        it = self.init_IT('FALSE', 'BODY')
        self.assertEqual(it.interpret(self.env), None, 'interpret method of IT should return None')

    def test_interpret_true_cond(self):
        # Test interpret method for if-condition evaluating to True
        self.init_env()
        it = self.init_IT('TRUE', 'BODY')
        self.assertEqual(it.interpret(self.env), 100, 'interpret method of IT should return 100')

if __name__ == '__main__':
    unittest.main()