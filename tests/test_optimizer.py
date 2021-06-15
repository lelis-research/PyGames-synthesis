from src.dsl import Constant, FallingFruitPosition, GreaterThan, IT, PlayerPosition, ReturnAction, Strategy
from src.Optimizer.optimizer import Optimizer
from unittest.mock import DEFAULT, patch, Mock
import unittest

class TestOptimizer(unittest.TestCase):

    def setUp(self):
        """
        Mock the ast that is to be optimized
        The ast looks like:

        if 10 > 0:
            return actions[0]
        """
        self.mock_const_1 = Mock()
        self.mock_const_1.__class__ = Constant
        self.mock_const_1.get_children.return_value = [10]

        def replace_child(child, i):
            self.mock_const_1.get_children.return_value = [child]
        self.mock_const_1.replace_child.side_effect = replace_child

        self.mock_const_2 = Mock()
        self.mock_const_2.__class__ = Constant
        self.mock_const_2.get_children.return_value = [0]

        def replace_child(child, i):
            self.mock_const_2.get_children.return_value = [child]
        self.mock_const_2.replace_child.side_effect = replace_child

        mock_gt = Mock()
        mock_gt.__class__ = GreaterThan
        mock_gt.get_children.return_value = [self.mock_const_1, self.mock_const_2]

        mock_ra = Mock()
        mock_ra.__class__ = ReturnAction
        mock_ra.get_children.return_value = [0]

        mock_it = Mock()
        mock_it.__class__ = IT
        mock_it.get_children.return_value = [mock_gt, mock_ra]

        self.mock_ast = Mock()
        self.mock_ast.__class__ = Strategy
        self.mock_ast.get_children.return_value = [mock_it]

    def test_get_const_range(self):
        optimizer = Optimizer(None, None, None, None)
        optimizer.ast = self.mock_ast
        correct_pbounds = {'Const1': (0.001, 100.001), 'Const2': (0.001, 100.001)}
        correct_orginal_values = [10, 0]
        correct_return_value = (correct_pbounds, correct_orginal_values)
        self.assertEqual(optimizer.get_const_range(), correct_return_value, 'Should return interval (0.001, 100.01)')

    def test_set_const_value(self):
        optimizer = Optimizer(None, None, None, None)
        optimizer.ast = self.mock_ast

        values = [70, 80]
        optimizer.set_const_value(values)
        self.assertEqual(self.mock_const_1.get_children()[0], 70, 'const_1 should have value 70')
        self.assertEqual(self.mock_const_2.get_children()[0], 80, 'const_2 should have value 80')

    def test_triage_optimize_called(self):
        triage_optimizer = Optimizer(None, True, 200, 2.5)
        triage_optimizer.triage_optimize = Mock()
        triage_optimizer.optimize(self.mock_ast, 0)
        triage_optimizer.triage_optimize.assert_called_once()

    def test_non_triage_optimize_called(self):
        nontriage_optimizer = Optimizer(None, False, 200, 2.5)
        nontriage_optimizer.non_triage_optimize = Mock()
        nontriage_optimizer.optimize(self.mock_ast, 0)
        nontriage_optimizer.non_triage_optimize.assert_called_once()

    def test_triage_optimize_true(self):
        self.score = 100
        def increase_score(x):
            self.score += 100
            return self.score - 100
        
        eval_funct = Mock()
        eval_funct.evaluate.side_effect = increase_score
        optimizer = Optimizer(eval_funct, True, 200, 2.5)
        results = optimizer.optimize(self.mock_ast, 0)
        self.assertTrue(results[2])

    def test_triage_optimize_false(self):
        eval_funct = Mock()
        eval_funct.evaluate.return_value = 100
        optimizer = Optimizer(eval_funct, True, 200, 2.5)
        results = optimizer.optimize(self.mock_ast, 0)
        self.assertFalse(results[2])

    def test_nontriage_optimize_true(self):
        self.score = 100
        def increase_score(x):
            self.score += 100
            return self.score - 100
        
        eval_funct = Mock()
        eval_funct.evaluate.side_effect = increase_score
        optimizer = Optimizer(eval_funct, False, 200, 2.5)
        results = optimizer.optimize(self.mock_ast, 0)
        self.assertTrue(results[2])

    def test_nontriage_optimize_false(self):
        eval_funct = Mock()
        eval_funct.evaluate.return_value = 0
        optimizer = Optimizer(eval_funct, False, 200, 2.5)
        results = optimizer.optimize(self.mock_ast, 0)
        self.assertFalse(results[2])
        

if __name__ == '__main__':
    unittest.main()