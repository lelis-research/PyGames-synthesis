"""
DSL_BUS.py 

Author: Olivier Vadiavaloo

Description:
This module implements sub-classes derived from src/DSL.py.
These sub-classes implement the grow methods of the base classes
so that the BUS algorithm can grow the programs accordingly.

"""
from random import choice
from pygame.constants import K_w, K_s, K_a, K_d
import numpy as np
import itertools
import src.dsl as baseDSL

"""
This class implements an AST node representing a constant.
"""
class Constant(baseDSL.Constant):

    def __init__(self):
        super(Constant, self).__init__()

"""
This is a class derived from the Node clas. It is interpreted as
choosing/returning an action among the available actions.
"""
class ReturnAction(baseDSL.ReturnAction):

    def __init__(self):
        super(ReturnAction, self).__init__()

    def grow(plist, psize):
        nplist = []

        programs = plist.get(psize-1, VarFromArray.className())
        
        if programs is not None:
            for p in programs:
                ra = ReturnAction.new(p)
                nplist.append(ra)
                yield ra


"""
This class represents a for loop in the DSL. It is interpreted as
a for-each loop where the program iterates over each element of the
provided iterable directly. For example,

for each x in coords:
    # loop body
"""
class ForEach(baseDSL.ForEach):

    def __init__(self):
        super(IT, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_iterable = [VarArray.className()]
        valid_loop_body = [IT.className(), ITE.className()]
        
        cost_combinations = itertools.product(range(psize-1), repeat=2)

        for cost in cost_combinations:

            if cost[0] + cost[1] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])

                if program_set_1 is not None and program_set_2 is not None:

                    for t1, p1 in program_set_1.items():
                        if t1 in valid_iterable:
                            for iter in p1:

                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_loop_body:
                                        for loop_body in p2:

                                            for_each = ForEach.new(iter, loop_body)
                                            nplist.append(for_each)
                                            yield for_each

        return nplist


"""
This class represents an if-then conditional statement in the DSL. It is
interpreted as the if-then conditional statements in general-purpose programming
languages
"""
class IT(baseDSL.IT):

    def __init__(self):
        super(IT, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_dsbs = [LessThan.className(), GreaterThan.className(), EqualTo.className(), NonPlayerObjectApproaching.className()]
        valid_return = [ReturnAction.className()]

        cost_combinations = itertools.product(range(psize-1), repeat=2)

        for cost in cost_combinations:

            if cost[0] + cost[1] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])

                if program_set_1 is not None and program_set_2 is not None:

                    for t1, p1 in program_set_1.items():
                        if t1 in valid_dsbs:    
                            for if_cond in p1:
                    
                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_return:
                                        for if_body in p2:
                                            
                                            it = IT.new(if_cond, if_body)
                                            nplist.append(it)
                                            yield it

        return nplist
    

"""
This class represents an if-then-else conditional statement in the 
DSL. It is interpreted as the if-then-else conditional statements in
general-purpose programming languages.
"""
class ITE(baseDSL.ITE):

    def __init__(self):
        super(ITE, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_dsbs = [LessThan.className(), GreaterThan.className(), EqualTo.className(), NonPlayerObjectApproaching.className()]
        valid_return = [ReturnAction.className(), IT.className()]

        cost_combinations = itertools.product(range(psize-1), repeat=3)
        
        for cost in cost_combinations:
            if cost[0] + cost[1] + cost[2] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])
                program_set_3 = plist.get(cost[2])

                if program_set_1 is not None and program_set_2 is not None and program_set_3 is not None:
                    
                    for t1, p1 in program_set_1.items():
                        if t1 in valid_dsbs:
                            for if_cond in p1:

                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_return:
                                        for if_body in p2:

                                            for t3, p3 in program_set_3.items():
                                                if t3 in valid_return:
                                                    for else_body in p3:

                                                        ite = ITE.new(if_cond, if_body, else_body)
                                                        nplist.append(ite)
                                                        yield ite

        return nplist


"""
This class implements a domain-specific function that returns
the x-position of the player on the screen.
"""
class PlayerPosition(baseDSL.PlayerPosition):

    def __init__(self):
        super(PlayerPosition, self).__init__()

"""
This class implements a domain-specific function that returns
the x-position of the non-player object. The non-player object
is the falling fruit in the Catcher game, while in Pong, it is
the ball.
"""
class NonPlayerObjectPosition(baseDSL.NonPlayerObjectPosition):

    def __init__(self):
        super(NonPlayerObjectPosition, self).__init__()


"""
This class implements a DSF that returns True if the non-player
object is moving towards the player and False otherwise.
"""
class NonPlayerObjectApproaching(baseDSL.NonPlayerObjectApproaching):

    def __init__(self):
        super(NonPlayerObjectApproaching, self).__init__()


"""
This class implements an AST node represent a list variable
"""
class VarArray(baseDSL.VarArray):
    
    def __init__(self):
        super(VarArray, self).__init__()


"""
This class implements an AST node representing a domain-specific scalar variable.
For instance, the player's paddle width.
"""
class VarScalar(baseDSL.VarScalar):

    def __init__(self):
        super(VarScalar, self).__init__()


"""
This class implements an AST node representing a domain-specific variable from
an array. For example, actions[0]
"""
class VarFromArray(baseDSL.VarFromArray):

    def __init__(self):
        super(VarFromArray, self).__init__()


"""
This class implements an AST node representing the '<' comparison
operator. It returns either True or False on calling its interpret
method.
"""
class LessThan(baseDSL.LessThan):

    def __init__(self):
        super(LessThan, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_nodes = [PlayerPosition.className(), NonPlayerObjectPosition.className(), Plus.className(),
            Minus.className(), Divide.className(), Times.className(), Constant.className()]

        cost_combinations = itertools.product(range(psize-1), repeat=2)
        
        for cost in cost_combinations:
            if cost[0] + cost[1] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])

                if program_set_1 is not None and program_set_2 is not None:
                    for t1, p1 in program_set_1.items():
                        if t1 in valid_nodes:
                            for left in p1:

                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_nodes:
                                        for right in p2:

                                            if left.to_string() != right.to_string():
                                                lt = LessThan.new(left, right)
                                                nplist.append(lt)
                                                yield lt

        return nplist


"""
This class implements an AST node representing the '>' comparison
operator. It returns either True or False on calling its interpret
method.
"""
class GreaterThan(baseDSL.GreaterThan):

    def __init__(self):
        super(GreaterThan, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_nodes = [PlayerPosition.className(), NonPlayerObjectPosition.className(), Plus.className(),
            Minus.className(), Divide.className(), Times.className(), Constant.className()]

        cost_combinations = itertools.product(range(psize-1), repeat=2)
        
        for cost in cost_combinations:
            if cost[0] + cost[1] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])

                if program_set_1 is not None and program_set_2 is not None:
                    for t1, p1 in program_set_1.items():
                        if t1 in valid_nodes:
                            for left in p1:

                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_nodes:
                                        for right in p2:

                                            if left.to_string() != right.to_string():
                                                gt = GreaterThan.new(left, right)
                                                nplist.append(gt)
                                                yield gt

        return nplist


"""
This class implements an AST node representing the '==' comparison
operator
"""
class EqualTo(baseDSL.EqualTo):

    def __init__(self):
        super(EqualTo, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_nodes = [PlayerPosition.className(), NonPlayerObjectPosition.className(), Plus.className(),
            Minus.className(), Divide.className(), Times.className(), Constant.className()]

        cost_combinations = itertools.product(range(psize-1), repeat=2)
        
        for cost in cost_combinations:
            if cost[0] + cost[1] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])

                if program_set_1 is not None and program_set_2 is not None:
                    for t1, p1 in program_set_1.items():
                        if t1 in valid_nodes:
                            for left in p1:

                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_nodes:
                                        for right in p2:

                                            if left.to_string() != right.to_string():
                                                eq = EqualTo.new(left, right)
                                                nplist.append(eq)
                                                yield eq

        return nplist


"""
This class implements an AST node representing the addition operator.
"""
class Plus(baseDSL.Plus):

    def __init__(self):
        super(Plus, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_nodes = [VarScalar.className(), PlayerPosition.className(), NonPlayerObjectPosition.className(), 
            Constant.className(), Times.className(), Minus.className(), Plus.className(), Divide.className()]

        cost_combinations = itertools.product(range(psize-1), repeat=2)

        for cost in cost_combinations:
            if cost[0] + cost[1] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])

                if program_set_1 is not None and program_set_2 is not None:
                    for t1, p1 in program_set_1.items():
                        if t1 in valid_nodes:
                            for left in p1:
                                
                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_nodes:
                                        for right in p2:
                                            if left.to_string() != '0' and right.to_string() != '0':
                                                plus = Plus.new(left, right)
                                                nplist.append(plus)
                                                yield plus
            
        return nplist


"""
This class implements an AST node representing the multiplication operator
"""
class Times(baseDSL.Times):

    def __init__(self):
        super(Times, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_nodes = [VarScalar.className(), PlayerPosition.className(), NonPlayerObjectPosition.className(),
            Constant.className(), Times.className(), Minus.className(), Plus.className(), Divide.className()]

        cost_combinations = itertools.product(range(psize-1), repeat=2)

        for cost in cost_combinations:
            if cost[0] + cost[1] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])

                if program_set_1 is not None and program_set_2 is not None:
                    for t1, p1 in program_set_1.items():
                        if t1 in valid_nodes:
                            for left in p1:
                                
                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_nodes:
                                        for right in p2:
                                            times = Times.new(left, right)
                                            eq = Times.new(right, left)
                                            is_equivalent = False
                                            for p in nplist:
                                                if p.to_string() == eq.to_string():
                                                    is_equivalent = True

                                            if not is_equivalent:
                                                nplist.append(times)
                                                yield times

        return nplist


"""
This class implements an AST node representing the minus operator
"""
class Minus(baseDSL.Minus):

    def __init__(self):
        super(Minus, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_nodes = [VarScalar.className(), PlayerPosition.className(), NonPlayerObjectPosition.className(),
            Constant.className(), Times.className(), Minus.className(), Plus.className(), Divide.className()]

        cost_combinations = itertools.product(range(psize-1), repeat=2)

        for cost in cost_combinations:
            if cost[0] + cost[1] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])

                if program_set_1 is not None and program_set_2 is not None:
                    for t1, p1 in program_set_1.items():
                        if t1 in valid_nodes:
                            for left in p1:
                                
                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_nodes:
                                        for right in p2:
                                            minus = Minus.new(left, right)
                                            if left.to_string() != right.to_string() and right.to_string() != '0':
                                                nplist.append(minus)
                                                yield minus

        return nplist


"""
This class implements an AST node representing the integer division operator
"""
class Divide(baseDSL.Divide):

    def __init__(self):
        super(Divide, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_nodes = [VarScalar.className(), PlayerPosition.className(), NonPlayerObjectPosition.className(),
            Constant.className(), Times.className(), Minus.className(), Plus.className(), Divide.className()]

        cost_combinations = itertools.product(range(psize-1), repeat=2)

        for cost in cost_combinations:
            if cost[0] + cost[1] + 1 == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])

                if program_set_1 is not None and program_set_2 is not None:
                    for t1, p1 in program_set_1.items():
                        if t1 in valid_nodes:
                            for left in p1:
                                
                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_nodes:
                                        for right in p2:
                                            if right.to_string() != '0' and left.to_string() != '0':
                                                if left.to_string() != right.to_string():
                                                    divide = Divide.new(left, right)
                                                    nplist.append(divide)
                                                    yield divide
        
        return nplist


"""
This class implements the initial symbol of the DSL.
"""
class Strategy(baseDSL.Strategy):

    def __init__(self):
        super(Strategy, self).__init__()

    def grow(plist, psize):
        nplist = []
        valid_first_statement = [IT.className(), ITE.className()]
        valid_next_statements = [Strategy.className(), ReturnAction.className(), type(None).__name__]

        cost_combinations = itertools.product(range(psize+1), repeat=2)

        for cost in cost_combinations:
            if cost[0] + cost[1] == psize:
                program_set_1 = plist.get(cost[0])
                program_set_2 = plist.get(cost[1])
                if cost[1] == 0 and program_set_2 is None:
                    program_set_2 = {}
                    program_set_2[type(None).__name__] = [None]

                if program_set_1 is not None and program_set_2 is not None:
                    for t1, p1 in program_set_1.items():
                        if t1 in valid_first_statement:
                            for statement in p1:

                                for t2, p2 in program_set_2.items():
                                    if t2 in valid_next_statements:
                                        for next_statements in p2:
                                            p = Strategy.new(statement, next_statements)
                                            nplist.append(p)
                                            yield p
        
        return nplist
