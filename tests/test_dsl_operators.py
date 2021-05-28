import unittest
from DSL import Minus, Times, Plus, Divide

class Operand:

    def __init__(self, value):
        self.size = 1
        self.value = value

    def getSize(self):
        return self.size

    def interpret(self, env):
        return self.value


class TestMinus(unittest.TestCase):

    def test_size_three(self):
        minus = Minus(Operand(5), Operand(5))
        self.assertEqual(minus.getSize(), 3, 'Minus object should have size 3')

    def test_size_change_minus_size(self):
        # Manually change the size of the Minus object
        minus = Minus(Operand(5), Operand(5))
        minus.size = 100
        self.assertEqual(minus.getSize(), 100, 'Minus object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the sizes of the args to the Minus class constructor
        left = Operand(5)
        left.size = 10
        right = Operand(5)
        right.size = 10
        minus = Minus(left, right)
        self.assertEqual(minus.getSize(), 21, 'Minus object should have size 21')

    def test_interpret(self):
        minus = Minus(Operand(100), Operand(35))
        self.assertEqual(minus.interpret({}), 65, 'interpret method of Minus object should return 65')


class TestAdd(unittest.TestCase):

    def test_size_three(self):
        plus = Plus(Operand(5), Operand(5))
        self.assertEqual(plus.getSize(), 3, 'Plus object should have size 3')

    def test_size_change_minus_size(self):
        # Manually change the size of the Plus object
        plus = Plus(Operand(5), Operand(5))
        plus.size = 100
        self.assertEqual(plus.getSize(), 100, 'Plus object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the sizes of the args to the Plus class constructor
        left = Operand(5)
        left.size = 10
        right = Operand(5)
        right.size = 10
        plus = Plus(left, right)
        self.assertEqual(plus.getSize(), 21, 'Plus object should have size 21')

    def test_interpret(self):
        plus = Plus(Operand(100), Operand(35))
        self.assertEqual(plus.interpret({}), 135, 'interpret method of Plus object should return 135')


class TestTimes(unittest.TestCase):

    def test_size_three(self):
        times = Times(Operand(5), Operand(5))
        self.assertEqual(times.getSize(), 3, 'Times object should have size 3')

    def test_size_change_minus_size(self):
        # Manually change the size of the Times object
        times = Times(Operand(5), Operand(5))
        times.size = 100
        self.assertEqual(times.getSize(), 100, 'Times object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the sizes of the args to the Times class constructor
        left = Operand(5)
        left.size = 10
        right = Operand(5)
        right.size = 10
        times = Times(left, right)
        self.assertEqual(times.getSize(), 21, 'Times object should have size 21')

    def test_interpret(self):
        times = Times(Operand(100), Operand(35))
        self.assertEqual(times.interpret({}), 3500, 'interpret method of Times object should return 3500')


class TestDivide(unittest.TestCase):

    def test_size_three(self):
        divide = Divide(Operand(5), Operand(5))
        self.assertEqual(divide.getSize(), 3, 'Divide object should have size 3')

    def test_size_change_minus_size(self):
        # Manually change the size of the Divide object
        divide = Divide(Operand(5), Operand(5))
        divide.size = 100
        self.assertEqual(divide.getSize(), 100, 'Divide object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the sizes of the args to the Divide class constructor
        left = Operand(5)
        left.size = 10
        right = Operand(5)
        right.size = 10
        divide = Divide(left, right)
        self.assertEqual(divide.getSize(), 21, 'Divide object should have size 21')

    def test_interpret_no_remainder(self):
        divide = Divide(Operand(100), Operand(5))
        self.assertEqual(divide.interpret({}), 20, 'interpret method of Divide object should return 20')

    def test_interpret_with_remainder(self):
        divide = Divide(Operand(100), Operand(3))
        self.assertEqual(divide.interpret({}), 33, 'interpret method of Divide object should return 33')

    def test_interpret_zero_division_error(self):
        divide = Divide(Operand(100), Operand(0))
        test_msg = 'interpret method of Divide object should raise ZeroDivisionError'
        with self.assertRaises(ZeroDivisionError, msg=test_msg) as cm:
            divide.interpret({})
    

if __name__ == '__main__':
    unittest.main()