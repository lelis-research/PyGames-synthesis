import unittest
from src.DSL import Minus, Times, Plus, Divide
from unittest.mock import Mock

def mockOperand(value):
        op = Mock()
        op.getSize.return_value = 1
        op.interpret.return_value = value
        return op


class TestMinus(unittest.TestCase):

    def test_size_three(self):
        minus = Minus(mockOperand(5), mockOperand(5))
        self.assertEqual(minus.getSize(), 3, 'Minus object should have size 3')

    def test_size_change_minus_size(self):
        # Manually change the size of the Minus object
        
        minus = Minus(mockOperand(5), mockOperand(5))
        minus.size = 100
        self.assertEqual(minus.getSize(), 100, 'Minus object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the sizes of the args to the Minus class constructor
        left = mockOperand(5)
        right = mockOperand(5)
        minus = Minus(left, right)
        left.getSize.return_value = 10
        right.getSize.return_value = 10
        self.assertEqual(minus.getSize(), 3, 'Minus object should have size 3')

    def test_interpret(self):
        minus = Minus(mockOperand(100), mockOperand(35))
        self.assertEqual(minus.interpret({}), 65, 'interpret method of Minus object should return 65')


class TestAdd(unittest.TestCase):

    def test_size_three(self):
        plus = Plus(mockOperand(5), mockOperand(5))
        self.assertEqual(plus.getSize(), 3, 'Plus object should have size 3')

    def test_size_change_minus_size(self):
        # Manually change the size of the Plus object
        plus = Plus(mockOperand(5), mockOperand(5))
        plus.size = 100
        self.assertEqual(plus.getSize(), 100, 'Plus object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the sizes of the args to the Plus class constructor
        left = mockOperand(5)
        right = mockOperand(5)
        plus = Plus(left, right)
        right.getSize.return_value = 10
        left.getSize.return_value = 10
        self.assertEqual(plus.getSize(), 3, 'Plus object should have size 3')

    def test_interpret(self):
        plus = Plus(mockOperand(100), mockOperand(35))
        self.assertEqual(plus.interpret({}), 135, 'interpret method of Plus object should return 135')


class TestTimes(unittest.TestCase):

    def test_size_three(self):
        times = Times(mockOperand(5), mockOperand(5))
        self.assertEqual(times.getSize(), 3, 'Times object should have size 3')

    def test_size_change_minus_size(self):
        # Manually change the size of the Times object
        times = Times(mockOperand(5), mockOperand(5))
        times.size = 100
        self.assertEqual(times.getSize(), 100, 'Times object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the sizes of the args to the Times class constructor
        left = mockOperand(5)
        right = mockOperand(5)
        times = Times(left, right)
        left.getSize.return_value = 10
        right.getSize.return_value = 10
        self.assertEqual(times.getSize(), 3, 'Times object should have size 3')

    def test_interpret(self):
        times = Times(mockOperand(100), mockOperand(35))
        self.assertEqual(times.interpret({}), 3500, 'interpret method of Times object should return 3500')


class TestDivide(unittest.TestCase):

    def test_size_three(self):
        divide = Divide(mockOperand(5), mockOperand(5))
        self.assertEqual(divide.getSize(), 3, 'Divide object should have size 3')

    def test_size_change_minus_size(self):
        # Manually change the size of the Divide object
        divide = Divide(mockOperand(5), mockOperand(5))
        divide.size = 100
        self.assertEqual(divide.getSize(), 100, 'Divide object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the sizes of the args to the Divide class constructor
        left = mockOperand(5)
        right = mockOperand(5)
        divide = Divide(left, right)
        left.getSize.return_value = 10
        right.getSize.return_value = 10
        self.assertEqual(divide.getSize(), 3, 'Divide object should have size 3')

    def test_interpret_no_remainder(self):
        divide = Divide(mockOperand(100), mockOperand(5))
        self.assertEqual(divide.interpret({}), 20, 'interpret method of Divide object should return 20')

    def test_interpret_with_remainder(self):
        divide = Divide(mockOperand(100), mockOperand(3))
        self.assertEqual(divide.interpret({}), 33, 'interpret method of Divide object should return 33')

    def test_interpret_zero_division_error(self):
        divide = Divide(mockOperand(100), mockOperand(0))
        test_msg = 'interpret method of Divide object should raise ZeroDivisionError'
        with self.assertRaises(ZeroDivisionError, msg=test_msg) as cm:
            divide.interpret({})
    

if __name__ == '__main__':
    unittest.main()