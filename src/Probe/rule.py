"""
rule.py

Author: Olivier Vadiavaloo

Description:
This module contains the Rule class which can be used to define the production
rules of a particular dsl.
"""

from src.dsl import *

class Rule:

    def __init__(self, top_symbol, sub_expressions=[]):
        assert top_symbol is not None, 'top_symbol of rule object cannot be None'
        self.top_symbol = top_symbol
        self.sub_expressions = sub_expressions

    def get_subexpressions_list(self):
        return self.sub_expressions.copy()

    def get_subexpr(self, index):
        return self.sub_expressions[index]

    def get_subexpr_count(self):
        return len(self.sub_expressions)

    def build_expression(self, sub_expr):
        assert len(sub_expr) == len(self.sub_expressions)
        assert type(sub_expr) is list

        for i in range(len(sub_expr)):
            assert type(sub_expr[i]) in self.get_subexpr(i)

        print('yield true')
        
        p = self.top_symbol()
        for child in sub_expr:
            p.add_child(child)

        return p

    def used_in(self, p):

        if isinstance(p, self.top_symbol):
            return True

        for child in p.get_children():
            if isinstance(child, self.top_symbol):
                return True
            
            if isinstance(child, Node) and self.used_in(child):
                return True

        return False

it_rule = Rule(
        IT,
        [
            set([GreaterThan, LessThan, EqualTo]),
            set([ReturnAction])
        ])

ite_rule = Rule(
    ITE,
    [
        set([GreaterThan, LessThan, EqualTo]),
        set([ReturnAction]),
        set([ReturnAction])
    ]
)

strategy_rule = Rule(
    Strategy,
    [
        set([IT, ITE]),
        set([IT, ITE, ReturnAction])
    ]
)

ra_rule = Rule(
    ReturnAction,
    [
        set([VarFromArray])
    ]
)

arithmetic_op_sub_expr = set([
    Constant,
    Times,
    Plus,
    Minus,
    Divide,
    FallingFruitPosition,
    PlayerPosition,
    VarScalar
])

plus_rule = Rule(Plus, [arithmetic_op_sub_expr, arithmetic_op_sub_expr])
minus_rule = Rule(Minus, [arithmetic_op_sub_expr, arithmetic_op_sub_expr])
divide_rule = Rule(Divide, [arithmetic_op_sub_expr, arithmetic_op_sub_expr])
times_rule = Rule(Times, [arithmetic_op_sub_expr, arithmetic_op_sub_expr])

comparison_op_sub_expr = set([
    VarScalar,
    Constant, 
    Minus, 
    Plus, 
    Times, 
    Divide, 
    FallingFruitPosition, 
    PlayerPosition
])

gt_rule = Rule(
    GreaterThan,
    [comparison_op_sub_expr, comparison_op_sub_expr]
)

lt_rule = Rule(
    LessThan,
    [comparison_op_sub_expr, comparison_op_sub_expr]
)

eq_rule = Rule(
    EqualTo,
    [comparison_op_sub_expr, comparison_op_sub_expr]
)

const_rule = Rule(
    Constant,
    [set([int, float])]
)

var_scalar_rule = Rule(
    VarScalar,
    [set([str])]
)

var_from_arr_rule = Rule(
    VarFromArray,
    [set([str]), set([int])]
)

fruit_pos_rule = Rule(
    FallingFruitPosition,
    []
)

player_pos_rule = Rule(
    PlayerPosition,
    []
)