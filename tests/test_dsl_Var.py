import unittest
from src.dsl import VarArray, VarScalar, VarFromArray, Constant
from unittest.mock import Mock

def Const(value):
    const = Mock()
    const.get_size.return_value = 1
    const.interpret.return_value = value
    type(const).__name__ = Constant.className()
    return const


class TestVarArray(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['action'] = [119, 83, None]

    def test_size_one(self):
        var_arr = VarArray.new('action')
        self.assertEqual(var_arr.get_size(), 1, 'VarArray object should have 1')

    def test_size_change_var_size(self):
        var_arr = VarArray.new('action')
        var_arr.size = 191
        self.assertEqual(var_arr.get_size(), 191, 'VarArray object should have size 191')

    def test_interpret(self):
        var_arr = VarArray.new('action')
        self.assertEqual(var_arr.interpret(self.env), [119, 83, None],
            'interpret method of VarArray object should return [119, 83, None]')


class TestVarScalar(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['SCALAR'] = 240

    def test_size_one(self):
        var_scalar = VarScalar.new('SCALAR')
        self.assertEqual(var_scalar.get_size(), 1, 'VarScalar object should have size 1')

    def test_size_change_var_size(self):
        var_scalar = VarScalar.new('SCALAR')
        var_scalar.size = 191
        self.assertEqual(var_scalar.get_size(), 191, 'VarScalar object should have size 191')

    def test_interpret(self):
        var_scalar = VarScalar.new('SCALAR')
        self.assertEqual(var_scalar.interpret(self.env), 240, 'interpret method of VarScalar object should return 240')


class TestVarFromArray(unittest.TestCase):

    def setUp(self):
        self.env = {}
        self.env['action'] = [119, 83, None]

    def test_size_one(self):
        var_from_arr = VarFromArray.new('action', Const(0))
        self.assertEqual(var_from_arr.get_size(), 2, 'VarFromArray object should have size 2')

    def test_size_change_var_size(self):
        var_from_arr = VarFromArray.new('action', Const(0))
        var_from_arr.size = 45
        self.assertEqual(var_from_arr.get_size(), 45, 'VarFromArray object should have size 45')

    def test_interpret_index_zero(self):
        var_from_arr = VarFromArray.new('action', Const(0))
        self.assertEqual(var_from_arr.interpret(self.env), 119, 'interpret method of VarFromArray object should return 119')

    def test_interpret_index_one(self):
        var_from_arr = VarFromArray.new('action', Const(1))
        self.assertEqual(var_from_arr.interpret(self.env), 83, 'interpret method of VarFromArray object should return 83')

    def test_interpret_index_two(self):
        var_from_arr = VarFromArray.new('action', Const(2))
        self.assertEqual(var_from_arr.interpret(self.env), None, 'interpret method of VarFromArray object should return None')

    def test_interpret_index_error(self):
        var_from_arr = VarFromArray.new('action', Const(100))
        test_msg = 'interpret method of VarFromArray object should raise IndexError'
        with self.assertRaises(IndexError, msg=test_msg) as cm:
            var_from_arr.interpret(self.env)


if __name__ == '__main__':
    unittest.main()