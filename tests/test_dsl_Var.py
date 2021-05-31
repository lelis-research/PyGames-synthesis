import unittest
from DSL import VarScalar, VarFromArray

class Const:

    def __init__(self, value):
        self.size = 1
        self.value = value
        self.__class__.__name__ = 'Constant'

    def getSize(self):
        return self.size

    def interpret(self, env):
        return self.value


class TestVarScalar(unittest.TestCase):

    def init_env(self):
        self.env = {}
        self.env['SCALAR'] = 240

    def test_size_one(self):
        var_scalar = VarScalar('SCALAR')
        self.assertEqual(var_scalar.getSize(), 1, 'VarScalar object should have size 1')

    def test_size_change_var_size(self):
        var_scalar = VarScalar('SCALAR')
        var_scalar.size = 191
        self.assertEqual(var_scalar.getSize(), 191, 'VarScalar object should have size 191')

    def test_interpret(self):
        self.init_env()
        var_scalar = VarScalar('SCALAR')
        self.assertEqual(var_scalar.interpret(self.env), 240, 'interpret method of VarScalar object should return 240')


class TestVarFromArray(unittest.TestCase):

    def init_env(self):
        self.env = {}
        self.env['action'] = [119, 83, None]

    def test_size_one(self):
        var_from_arr = VarFromArray('action', Const(0))
        self.assertEqual(var_from_arr.getSize(), 2, 'VarFromArray object should have size 1')

    def test_size_change_var_size(self):
        var_from_arr = VarFromArray('action', Const(0))
        var_from_arr.size = 45
        self.assertEqual(var_from_arr.getSize(), 45, 'VarFromArray object should have size 45')

    def test_interpret_index_zero(self):
        self.init_env()
        var_from_arr = VarFromArray('action', Const(0))
        self.assertEqual(var_from_arr.interpret(self.env), 119, 'interpret method of VarFromArray object should return 119')

    def test_interpret_index_one(self):
        self.init_env()
        var_from_arr = VarFromArray('action', Const(1))
        self.assertEqual(var_from_arr.interpret(self.env), 83, 'interpret method of VarFromArray object should return 83')

    def test_interpret_index_two(self):
        self.init_env()
        var_from_arr = VarFromArray('action', Const(2))
        self.assertEqual(var_from_arr.interpret(self.env), None, 'interpret method of VarFromArray object should return None')

    def test_interpret_index_error(self):
        self.init_env()
        var_from_arr = VarFromArray('action', Const(100))
        test_msg = 'interpret method of VarFromArray object should raise IndexError'
        with self.assertRaises(IndexError, msg=test_msg) as cm:
            var_from_arr.interpret(self.env)


if __name__ == '__main__':
    unittest.main()