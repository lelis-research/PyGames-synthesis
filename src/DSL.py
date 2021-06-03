"""
DSL.py 

Author: Olivier Vadiavaloo

Description:
This module implements the nodes used to create Abstract-Syntax Trees (ASTs)
that represent programs written in the DSL designed for playing the Catcher game.

"""
from random import choice
from pygame.constants import K_w, K_s, K_a, K_d
import numpy as np
import itertools

"""
This is a base class representing the Node of an abstract-
syntax tree for the DSL implemented in this module. All other
classes in this module are derived from this Node class.
"""
class Node:

    def __init__(self):
        self.size = 1
        self.current_child_num = 0
        self.max_number_children = 0
        self.children = []

        self.statename = 'state'
        self.actionname = 'actions'

    def add_child(self, child):
        assert len(self.children) < self.max_number_children
        self.children.append(child)
        self.current_child_num += 1
        
        if child is not None:
            self.size += child.getSize()

    def replace_child(self, child, i):
        if self.children[i] is not None:
            self.size -= self.children[i].getSize()

        if child is not None:
            self.size += child.getSize()

        self.children[i] = child

    def getSize(self):
        return self.size

    def toString(self, indent=0):
        raise Exception("Unimplemented method: toStrng")

    def interpret(self):
        raise Exception("Unimplemented method: interpret")

    def get_children(self):
        return self.children.copy()

    def get_current_child_num(self):
        return self.current_child_num

    def get_max_number_children(self):
        return self.max_number_children

    @classmethod
    def get_valid_children_types(self):
        return self.valid_children_types

    @classmethod
    def className(cls):
        return cls.__name__

    @staticmethod
    def grow(plist, psize):
        pass


"""
This class implements an AST node representing a constant.
"""
class Constant(Node):

    def __init__(self):
        super(Constant, self).__init__()
        self.max_number_children = 0

    @classmethod
    def new(cls, value):
        assert value in np.arange(0, 101, 0.01)
        inst = cls()
        inst.value = value
        
        return inst

    def toString(self, indent=0):
        return f"{self.value}"

    def interpret(self, env):
        return self.value


"""
This is a class derived from the Node clas. It is interpreted as
choosing/returning an action among the available actions.
"""
class ReturnAction(Node):

    def __init__(self):
        super(ReturnAction, self).__init__()
        self.max_number_children = 1

    @classmethod
    def new(cls, action):
        inst = cls()
        inst.add_child(action)

        return inst

    def toString(self, indent=0):
        action = self.get_children()[0]
        return f"return {action.toString()}"

    def interpret(self, env):
        action = self.get_children()[0]
        return action.interpret(env)


"""
This class represents an if-then conditional statement in the DSL. It is
interpreted as the if-then conditional statements in general-purpose programming
languages
"""
class IT(Node):

    def __init__(self):
        super(IT, self).__init__()
        self.max_number_children = 2

    @classmethod
    def new(cls, condition, if_body):
        assert type(if_body).__name__ == ReturnAction.className()
        inst = cls()
        inst.add_child(condition)
        inst.add_child(if_body)

        return inst

    def toString(self, indent=0):
        tab = ""
        for i in range(indent):
            tab += "\t"

        condition = self.get_children()[0]
        if_body = self.get_children()[1]
        
        it_string = f"""{tab}if {condition.toString()}:\n"""
        it_string += f"""{tab}\t{if_body.toString()}"""
        return it_string

    def interpret(self, env):
        condition = self.get_children()[0]
        if_body = self.get_children()[1]

        if condition.interpret(env):
            return if_body.interpret(env)
    

"""
This class represents an if-then-else conditional statement in the 
DSL. It is interpreted as the if-then-else conditional statements in
general-purpose programming languages.
"""
class ITE(Node):

    def __init__(self):
        super(ITE, self).__init__()
        self.max_number_children = 3

    @classmethod
    def new(cls, condition, if_body, else_body):
        assert type(if_body).__name__ == ReturnAction.className()
        assert type(else_body).__name__ == ReturnAction.className()
        inst = cls()
        inst.add_child(condition)
        inst.add_child(if_body)
        inst.add_child(else_body)

        return inst

    def toString(self, indent=0):
        tab = ""
        for i in range(indent):
            tab += "\t"
        
        condition = self.get_children()[0]
        if_body = self.get_children()[1]
        else_body = self.get_children()[2]

        ite_string = f"""{tab}if {condition.toString()}:\n"""
        ite_string += f"""{tab}\t{if_body.toString()}\n"""
        ite_string += f"""{tab}else:\n"""
        ite_string += f"""{tab}\t{else_body.toString()}"""
        return ite_string

    def interpret(self, env):
        condition = self.get_children()[0]
        if_body = self.get_children()[1]
        else_body = self.get_children()[2]

        if condition.interpret(env):
            return if_body.interpret(env)
        else:
            return else_body.interpret(env)


"""
This class implements a domain-specific function that returns
the x-position of the player on the screen.
"""
class PlayerPosition(Node):

    def __init__(self):
        super(PlayerPosition, self).__init__()
        self.max_number_children = 0

    def toString(self, indent=0):
        return PlayerPosition.className()

    def interpret(self, env):
        return env[self.statename]['player_position']


"""
This class implements a domain-specific function that returns
the y-position of the falling fruit to be caught by the player.
"""
class FallingFruitPosition(Node):

    def __init__(self):
        super(FallingFruitPosition, self).__init__()
        self.max_number_children = 0

    def toString(self, indent=0):
        return FallingFruitPosition.className()

    def interpret(self, env):
        return env[self.statename]['fruit_position']


"""
This class implements an AST node representing a domain-specific scalar variable.
For instance, the player's paddle width.
"""
class VarScalar(Node):

    def __init__(self):
        super(VarScalar, self).__init__()
        self.max_number_children = 0

    @classmethod
    def new(cls, name):
        inst = cls()
        inst.name = name

        return inst

    def toString(self, indent=0):
        return f"{self.name}"

    def interpret(self, env):
        return env[self.name]


"""
This class implements an AST node representing a domain-specific variable from
an array. For example, actions[0]
"""
class VarFromArray(Node):

    def __init__(self):
        super(VarFromArray, self).__init__()
        self.max_number_children = 1

    @classmethod
    def new(cls, name, index):
        assert type(index).__name__ == Constant.className()
        inst = cls()
        inst.add_child(index)
        inst.name = name

        return inst
    
    def toString(self, indent=0):
        index = self.get_children()[0]
        return f"{self.name}[{index.toString()}]"

    def interpret(self, env):
        index = self.get_children()[0]
        return env[self.name][index.interpret(env)]


"""
This class implements an AST node representing the '<' comparison
operator. It returns either True or False on calling its interpret
method.
"""
class LessThan(Node):

    def __init__(self):
        super(LessThan, self).__init__()
        self.max_number_children = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def toString(self, indent=0):
        return f"{self.get_children()[0].toString()} < {self.get_children()[1].toString()}"

    def interpret(self, env):
        return self.get_children()[0].interpret(env) < self.get_children()[1].interpret(env)


"""
This class implements an AST node representing the '>' comparison
operator. It returns either True or False on calling its interpret
method.
"""
class GreaterThan(Node):

    def __init__(self):
        super(GreaterThan, self).__init__()
        self.max_number_children = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def toString(self, indent=0):
        return f"{self.get_children()[0].toString()} > {self.get_children()[1].toString()}"

    def interpret(self, env):
        return self.get_children()[0].interpret(env) > self.get_children()[1].interpret(env)


"""
This class implements an AST node representing the '==' comparison
operator
"""
class EqualTo(Node):

    def __init__(self):
        super(EqualTo, self).__init__()
        self.max_number_children = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def toString(self, indent=0):
        return f"{self.get_children()[0].toString()} == {self.get_children()[1].toString()}"

    def interpret(self, env):
        return self.get_children()[0].interpret(env) == self.get_children()[1].interpret(env)


"""
This class implements an AST node representing the addition operator.
"""
class Plus(Node):

    def __init__(self):
        super(Plus, self).__init__()
        self.max_number_children = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def toString(self, indent=0):
        return f"({self.get_children()[0].toString()} + {self.get_children()[1].toString()})"

    def interpret(self, env):
        return self.get_children()[0].interpret(env) + self.get_children()[1].interpret(env)


"""
This class implements an AST node representing the multiplication operator
"""
class Times(Node):

    def __init__(self):
        super(Times, self).__init__()
        self.max_number_children = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def toString(self, indent=0):
        return f"({self.get_children()[0].toString()} * {self.get_children()[1].toString()})"

    def interpret(self, env):
        return self.get_children()[0].interpret(env) * self.get_children()[1].interpret(env)


"""
This class implements an AST node representing the minus operator
"""
class Minus(Node):

    def __init__(self):
        super(Minus, self).__init__()
        self.max_number_children = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def toString(self, indent=0):
        return f"({self.get_children()[0].toString()} - {self.get_children()[1].toString()})"

    def interpret(self, env):
        return self.get_children()[0].interpret(env) - self.get_children()[1].interpret(env)


"""
This class implements an AST node representing the integer division operator
"""
class Divide(Node):

    def __init__(self):
        super(Divide, self).__init__()
        self.max_number_children = 2

    @classmethod
    def new(cls, left, right):
        inst = cls()
        inst.add_child(left)
        inst.add_child(right)

        return inst

    def toString(self, indent=0):
        return f"({self.get_children()[0].toString()} // {self.get_children()[1].toString()})"

    
    def interpret(self, env):
        return self.get_children()[0].interpret(env) // self.get_children()[1].interpret(env)


"""
This class implements the initial symbol of the DSL.
"""
class Strategy(Node):

    def __init__(self, statement, next_statements):
        super(Strategy, self).__init__()
        self.size = 0
        self.max_number_children = 2

    @classmethod
    def new(cls, statement, next_statements):
        assert type(statement).__name__ in [IT.className(), ITE.className()]
        assert type(next_statements).__name__ in [Strategy.className(), ReturnAction.className(), type(None).__name__]
        inst = cls()
        inst.add_child(statement)
        inst.add_child(next_statements)

        return inst

    def toString(self, indent=0):
        statement = self.get_children()[0]
        next_statements = self.get_children()[1]

        strategy_string = f"{statement.toString(0)}\n"
        if next_statements is not None:
            strategy_string += f"{next_statements.toString()}"

        return strategy_string

    def interpret(self, env):
        statement = self.get_children()[0]
        next_statements = self.get_children()[1]

        res = statement.interpret(env)
        if res is None and next_statements is not None:
            return next_statements.interpret(env)

        return res