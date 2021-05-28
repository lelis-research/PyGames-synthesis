import unittest
from DSL import Strategy, IT

class FirstStatement:

    def __init__(self, value):
        self.size = 1
        self.value = value
        type(self).__name__ = IT.className()

    def getSize(self):
        return self.size

    def interpret(self, env):
        return self.value


class NextStatement:

    def __init__(self, value):
        self.size = 1
        self.value = value
        type(self).__name__ = Strategy.className()

    def getSize(self):
        return self.size
    
    def interpret(self, env):
        return self.value


class TestStrategy(unittest.TestCase):

    def test_size_three(self):
        s = Strategy(FirstStatement(90), NextStatement(100))
        self.assertEqual(s.getSize(), 2, 'Strategy object should have size 3')

    def test_size_none_next_statement(self):
        s = Strategy(FirstStatement(90), None)
        self.assertEqual(s.getSize(), 1, 'Strategy object should have size 2')

    def test_size_change_strategy_size(self):
        s = Strategy(FirstStatement(10), NextStatement(6))
        s.size = 90
        self.assertEqual(s.getSize(), 90, 'Strategy object should have size 90')

    def test_raises_assertion_error(self):
        first_statement = FirstStatement(10)
        first_statement.__class__.__name__ = 'FirstStatement'
        test_msg = 'Strategy constructor should raise AssertionError'
        with self.assertRaises(AssertionError, msg=test_msg) as cm:
            Strategy(first_statement, None)

        first_statement.__class__.__name__ = IT.className()
        with self.assertRaises(AssertionError, msg=test_msg) as cm:
            Strategy(first_statement, first_statement)

    def test_interpret_first_statement_only(self):
        first = FirstStatement(60)
        second = NextStatement(80)
        s = Strategy(first, second)
        self.assertEqual(s.interpret({}), 60, 'interpret method of Strategy object should return 60')

        second = None
        s = Strategy(first, second)
        self.assertEqual(s.interpret({}), 60, 'interpret method of Strategy object should return 60')

    def test_interpret_none_first_statement(self):
        first = FirstStatement(None)
        second = NextStatement(80)
        s = Strategy(first, second)
        self.assertEqual(s.interpret({}), 80, 'interpret method of Strategy object should return 80')

    def test_interpret_both_none(self):
        first = FirstStatement(None)
        second = None
        s = Strategy(first, second)
        self.assertEqual(s.interpret({}), None, 'interpret method of Strategy object should return None')


if __name__ == '__main__':
    unittest.main()