import unittest
from src.DSL import LessThan, GreaterThan, EqualTo
from unittest.mock import Mock

def mockOperand(value):
    op = Mock()
    op.getSize.return_value = 1
    op.interpret.return_value = value
    return op


class TestLessThan(unittest.TestCase):

    def test_size_three(self):
        lt = LessThan.new(mockOperand(5), mockOperand(3))
        self.assertEqual(lt.getSize(), 3, 'LessThan object should have size 3')

    def test_size_change_lessThan_size(self):
        # Manually change lt.size to 100
        lt = LessThan.new(mockOperand(5), mockOperand(5))
        lt.size = 100
        self.assertEqual(lt.getSize(), 100, 'LessThan object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the Operand sizes
        left = mockOperand(5)
        right = mockOperand(14)
        lt = LessThan.new(left, right)
        left.getSize.return_value = 10
        right.getSize.return_value = 10
        self.assertEqual(lt.getSize(), 3, 'LessThan object should have size 3')

    def test_interpret_true(self):
        lt = LessThan.new(mockOperand(3), mockOperand(10))
        self.assertEqual(type(lt.interpret({})).__name__, 'bool', 'interpret method of LessThan object should return a \'bool\'')
        self.assertEqual(lt.interpret({}), True, 'interpret method of LessThan object should return True')

    def test_interpret_false(self):
        lt = LessThan.new(mockOperand(88), mockOperand(10))
        self.assertEqual(type(lt.interpret({})).__name__, 'bool', 'interpret method of LessThan object should return a \'bool\'')
        self.assertEqual(lt.interpret({}), False, 'interpret method of LessThan object should return False')

        lt = LessThan.new(mockOperand(77), mockOperand(77))
        self.assertEqual(lt.interpret({}), False, 'interpret method of LessThan object should return False')


class TestGreaterThan(unittest.TestCase):

    def test_size_three(self):
        gt = GreaterThan.new(mockOperand(5), mockOperand(3))
        self.assertEqual(gt.getSize(), 3, 'GreaterThan object should have size 3')

    def test_size_change_lessThan_size(self):
        # Manually change gt.size to 100
        gt = GreaterThan.new(mockOperand(5), mockOperand(5))
        gt.size = 100
        self.assertEqual(gt.getSize(), 100, 'GreaterThan object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the Operand sizes
        left = mockOperand(5)
        right = mockOperand(14)
        gt = GreaterThan.new(left, right)
        left.getSize.return_value = 10
        right.getSize.return_value = 14
        self.assertEqual(gt.getSize(), 3, 'GreaterThan object should have size 3')

    def test_interpret_true(self):
        gt = GreaterThan.new(mockOperand(10), mockOperand(3))
        self.assertEqual(type(gt.interpret({})).__name__, 'bool', 'interpret method of GreaterThan object should return a \'bool\'')
        self.assertEqual(gt.interpret({}), True, 'interpret method of GreaterThan object should return True')

    def test_interpret_false(self):
        gt = GreaterThan.new(mockOperand(10), mockOperand(88))
        self.assertEqual(type(gt.interpret({})).__name__, 'bool', 'interpret method of GreaterThan object should return a \'bool\'')
        self.assertEqual(gt.interpret({}), False, 'interpret method of GreaterThan object should return False')

        gt = GreaterThan.new(mockOperand(77), mockOperand(77))
        self.assertEqual(gt.interpret({}), False, 'interpret method of GreaterThan object should return False')


class TestEqualTo(unittest.TestCase):

    def test_size_three(self):
        eq = EqualTo.new(mockOperand(5), mockOperand(3))
        self.assertEqual(eq.getSize(), 3, 'EqualTo object should have size 3')

    def test_size_change_lessThan_size(self):
        # Manually change eq.size to 100
        eq = EqualTo.new(mockOperand(5), mockOperand(5))
        eq.size = 100
        self.assertEqual(eq.getSize(), 100, 'EqualTo object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the mockOperand sizes
        left = mockOperand(5)
        right = mockOperand(14)
        eq = EqualTo.new(left, right)
        left.getSize.return_value = 50
        right.getSize.return_value = 10
        self.assertEqual(eq.getSize(), 3, 'EqualTo object should have size 3')

    def test_interpret_true(self):
        eq = EqualTo.new(mockOperand(60), mockOperand(60))
        self.assertEqual(type(eq.interpret({})).__name__, 'bool', 'interpret method of EqualTo object should return a \'bool\'')
        self.assertEqual(eq.interpret({}), True, 'interpret method of EqualTo object should return True')

    def test_interpret_false(self):
        eq = EqualTo.new(mockOperand(88), mockOperand(10))
        self.assertEqual(type(eq.interpret({})).__name__, 'bool', 'interpret method of EqualTo object should return a \'bool\'')
        self.assertEqual(eq.interpret({}), False, 'interpret method of EqualTo object should return False')

        eq = EqualTo.new(mockOperand(45), mockOperand(92))
        self.assertEqual(eq.interpret({}), False, 'interpret method of EqualTo object should return False')


if __name__ == '__main__':
    unittest.main()