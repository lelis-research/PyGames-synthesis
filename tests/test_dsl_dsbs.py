import unittest
from DSL import LessThan, GreaterThan, EqualTo

class Operand:

    def __init__(self, value):
        self.size = 1
        self.value = value
    
    def getSize(self):
        return self.size

    def interpret(self, env):
        return self.value


class TestLessThan(unittest.TestCase):

    def test_size_three(self):
        lt = LessThan(Operand(5), Operand(3))
        self.assertEqual(lt.getSize(), 3, 'LessThan object should have size 3')

    def test_size_change_lessThan_size(self):
        # Manually change lt.size to 100
        lt = LessThan(Operand(5), Operand(5))
        lt.size = 100
        self.assertEqual(lt.getSize(), 100, 'LessThan object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the Operand sizes
        left = Operand(5)
        left.size = 50
        right = Operand(14)
        right.size = 10
        lt = LessThan(left, right)
        self.assertEqual(lt.getSize(), 61, 'LessThan object should have size 61')

    def test_interpret_true(self):
        lt = LessThan(Operand(3), Operand(10))
        self.assertEqual(type(lt.interpret({})).__name__, 'bool', 'interpret method of LessThan object should return a \'bool\'')
        self.assertEqual(lt.interpret({}), True, 'interpret method of LessThan object should return True')

    def test_interpret_false(self):
        lt = LessThan(Operand(88), Operand(10))
        self.assertEqual(type(lt.interpret({})).__name__, 'bool', 'interpret method of LessThan object should return a \'bool\'')
        self.assertEqual(lt.interpret({}), False, 'interpret method of LessThan object should return False')

        lt = LessThan(Operand(77), Operand(77))
        self.assertEqual(lt.interpret({}), False, 'interpret method of LessThan object should return False')


class TestGreaterThan(unittest.TestCase):

    def test_size_three(self):
        gt = GreaterThan(Operand(5), Operand(3))
        self.assertEqual(gt.getSize(), 3, 'GreaterThan object should have size 3')

    def test_size_change_lessThan_size(self):
        # Manually change gt.size to 100
        gt = GreaterThan(Operand(5), Operand(5))
        gt.size = 100
        self.assertEqual(gt.getSize(), 100, 'GreaterThan object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the Operand sizes
        left = Operand(5)
        left.size = 50
        right = Operand(14)
        right.size = 10
        gt = GreaterThan(left, right)
        self.assertEqual(gt.getSize(), 61, 'GreaterThan object should have size 61')

    def test_interpret_true(self):
        gt = GreaterThan(Operand(10), Operand(3))
        self.assertEqual(type(gt.interpret({})).__name__, 'bool', 'interpret method of GreaterThan object should return a \'bool\'')
        self.assertEqual(gt.interpret({}), True, 'interpret method of GreaterThan object should return True')

    def test_interpret_false(self):
        gt = GreaterThan(Operand(10), Operand(88))
        self.assertEqual(type(gt.interpret({})).__name__, 'bool', 'interpret method of GreaterThan object should return a \'bool\'')
        self.assertEqual(gt.interpret({}), False, 'interpret method of GreaterThan object should return False')

        gt = GreaterThan(Operand(77), Operand(77))
        self.assertEqual(gt.interpret({}), False, 'interpret method of GreaterThan object should return False')


class TestEqualTo(unittest.TestCase):

    def test_size_three(self):
        eq = EqualTo(Operand(5), Operand(3))
        self.assertEqual(eq.getSize(), 3, 'EqualTo object should have size 3')

    def test_size_change_lessThan_size(self):
        # Manually change eq.size to 100
        eq = EqualTo(Operand(5), Operand(5))
        eq.size = 100
        self.assertEqual(eq.getSize(), 100, 'EqualTo object should have size 100')

    def test_size_change_args_size(self):
        # Manually change the Operand sizes
        left = Operand(5)
        left.size = 50
        right = Operand(14)
        right.size = 10
        eq = EqualTo(left, right)
        self.assertEqual(eq.getSize(), 61, 'EqualTo object should have size 61')

    def test_interpret_true(self):
        eq = EqualTo(Operand(60), Operand(60))
        self.assertEqual(type(eq.interpret({})).__name__, 'bool', 'interpret method of EqualTo object should return a \'bool\'')
        self.assertEqual(eq.interpret({}), True, 'interpret method of EqualTo object should return True')

    def test_interpret_false(self):
        eq = EqualTo(Operand(88), Operand(10))
        self.assertEqual(type(eq.interpret({})).__name__, 'bool', 'interpret method of EqualTo object should return a \'bool\'')
        self.assertEqual(eq.interpret({}), False, 'interpret method of EqualTo object should return False')

        eq = EqualTo(Operand(45), Operand(92))
        self.assertEqual(eq.interpret({}), False, 'interpret method of EqualTo object should return False')


if __name__ == '__main__':
    unittest.main()