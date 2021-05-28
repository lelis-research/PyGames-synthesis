import unittest
from DSL import ITE, ReturnAction

class TestITE(unittest.TestCase):

    class IF_COND:

        def __init__(self, cond):
            self.size = 1
            self.cond = cond

        def getSize(self):
            return self.size

        def interpret(self, env):
            return env[self.cond]

    class BODY:

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
        self.env['IF_BODY'] = 100
        self.env['ELSE_BODY'] = 53

    def init_ITE(self, if_cond, if_body, else_body):
        return ITE(TestITE.IF_COND(if_cond), TestITE.BODY(if_body), TestITE.BODY(else_body))

    def test_size_four(self):
        ite = self.init_ITE('TRUE', 'IF_BODY', 'ELSE_BODY')
        self.assertEqual(ite.getSize(), 4, 'ITE object should have size 4')

    def test_size_change_it_size(self):
        ite = self.init_ITE('TRUE', 'IF_BODY', 'ELSE_BODY')

        # Manually change the size of the ite instance
        ite.size = 100
        self.assertEqual(ite.getSize(), 100, 'ITE object should have size 100')

    def test_size_change_arg_size(self):
        if_cond = TestITE.IF_COND('TRUE')
        if_body = TestITE.BODY('IF_BODY')
        else_body = TestITE.BODY('ELSE_BODY')

        # Manually change the size of the arguments to the ITE constructor
        if_cond.size = 10
        if_body.size = 10
        else_body.size = 10
        ite = ITE(if_cond, if_body, else_body)
        self.assertEqual(ite.getSize(), 31, 'ITE object should have size 31')

    def test_interpret_false(self):
        # Test the interpret method with the if-condition evaluating to False
        self.init_env()
        ite = self.init_ITE('FALSE', 'IF_BODY', 'ELSE_BODY')
        self.assertEqual(ite.interpret(self.env), 53, 'interpret method of ITE object should return 53')

    def test_interpret_true(self):
        # Test the interpret method with the if-condition evaluating to True
        self.init_env()
        ite = self.init_ITE('TRUE', 'IF_BODY', 'ELSE_BODY')
        self.assertEqual(ite.interpret(self.env), 100, 'interpret method of ITE object should return 100')


if __name__ == '__main__':
    unittest.main()