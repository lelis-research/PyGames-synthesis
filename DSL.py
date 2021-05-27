"""
DSL.py 

Author: Olivier Vadiavaloo

Description:
This module implements the nodes used to create Abstract-Syntax Trees (ASTs)
that represent programs written in the DSL designed for playing the Catcher game.

"""
from pygame.constants import K_w, K_s, K_a, K_d
import numpy as np

"""
This is a base class representing the Node of an abstract-
syntax tree for the DSL implemented in this module. All other
classes in this module are derived from this Node class.
"""
class Node:

    def __init__(self):
        self.size = 0
        self.statename = 'state'
        self.actionname = 'actions'

    def getSize(self):
        return self.size

    def toString(self):
        raise Exception("Unimplemented method: toStrng")

    def interpret(self):
        raise Exception("Unimplemented method: interpret")

    @classmethod
    def grow(plist, nplist):
        pass

    @classmethod
    def className(cls):
        return cls.__name__


"""
This is a class derived from the Node clas. It is interpreted as
choosing/returning an action among the available actions.
"""
class ReturnAction(Node):

    def __init__(self, action):
        super(ReturnAction, self).__init__()
        self.size = 1 + action.getSize()
        self.action = action

    def toString(self):
        return f"return {self.action.toString()}"

    def interpret(self, env):
        return self.action.interpret(env)


"""
This class represents an if-then conditional statement in the DSL. It is
interpreted as the if-then conditional statements in general-purpose programming
languages
"""
class IT(Node):

    def __init__(self, condition, if_body):
        super(IT, self).__init__()
        assert type(if_body).__name__ == ReturnAction.className()
        self.size = 1 + condition.getSize() + if_body.getSize()
        self.condition = condition
        self.if_body = if_body

    def toString(self, indent):
        tab = ""
        for i in range(indent):
            tab += "\t"
        
        it_string = f"""{tab}if {self.condition.toString()}:\n\t"""
        it_string += f"""{self.if_body.toString()}"""
        return it_string

    def interpret(self, env):
        if self.condition.interpret(env):
            return self.if_body.interpret(env)


"""
This class represents an if-then-else conditional statement in the 
DSL. It is interpreted as the if-then-else conditional statements in
general-purpose programming languages.
"""
class ITE(Node):

    def __init__(self, condition, if_body, else_body):
        super(ITE, self).__init__()
        assert type(if_body).__name__ == ReturnAction.className()
        assert type(else_body).__name__ == ReturnAction.className()
        self.size = 1 + condition.getSize() + if_body.getSize() + else_body.getSize()
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def toString(self, indent):
        tab = ""
        for i in range(indent):
            tab += "\t"
        
        ite_string = f"""{tab}if {self.condition.toString()}:\n\t"""
        ite_string += f"""{self.if_body.toString()}\n"""
        ite_string += f"""{tab}else:\n\t"""
        ite_string += f"""{self.else_body.toString()}"""
        return ite_string

    def interpret(self, env):
        if self.condition.interpret(env):
            return self.if_body.interpret(env)
        else:
            return self.else_body.interpret(env)


"""
This class implements a domain-specific function that returns
the x-position of the player on the screen.
"""
class PlayerPosition(Node):

    def __init__(self):
        super(PlayerPosition, self).__init__()
        self.size = 1

    def toString(self):
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
        self.size = 1

    def toString(self):
        return FallingFruitPosition.className()

    def interpret(self, env):
        return env[self.statename]['fruit_position']


"""
This class implements an AST node representing a domain-specific scalar variable.
For instance, the player's paddle width.
"""
class VarScalar(Node):

    def __init__(self, name):
        super(VarScalar, self).__init__()
        self.size = 1
        self.name = name

    def toString(self):
        return f"{self.name}"

    def interpret(self, env):
        return env[self.name]


"""
This class implements an AST node representing a domain-specific variable from
an array. For example, actions[0]
"""
class VarFromArray(Node):

    def __init__(self, name, index):
        super(VarFromArray, self).__init__()
        self.name = name
        self.index = index
    
    def toString(self):
        return f"{self.name}[{self.index}]"

    def interpret(self, env):
        return env[self.name][self.index]


"""
This class implements an AST node representing the '<' comparison
operator. It returns either True or False on calling its interpret
method.
"""
class LessThan(Node):

    def __init__(self, left, right):
        super(LessThan, self).__init__()
        self.size = 1 + left.getSize() + right.getSize()
        self.left = left
        self.right = right

    def toString(self):
        return f"{self.left} < {self.right}"

    def interpret(self, env):
        return self.left.interpret(env) < self.right.interpret(env)


"""
This class implements an AST node representing the '>' comparison
operator. It returns either True or False on calling its interpret
method.
"""
class GreaterThan(Node):

    def __init__(self, left, right):
        super(GreaterThan, self).__init__()
        self.size = 1 + left.getSize() + right.getSize()
        self.left = left
        self.right = right

    def toString(self):
        return f"{self.left} > {self.right}"

    def interpret(self, env):
        return self.left.interpret(env) > self.right.interpret(env)


"""
This class implements an AST node representing the '==' comparison
operator
"""
class EqualTo(Node):

    def __init__(self, left, right):
        super(EqualTo, self).__init__()
        self.size = 1 + left.getSize() + right.getSize()
        self.left = left
        self.right = right

    def toString(self):
        return f"{self.left} == {self.right}"

    def interpret(self, env):
        return self.left.interpret(env) == self.right.interpret(env)


"""
This class implements an AST node representing the addition operator.
"""
class Plus(Node):

    def __init__(self, left, right):
        super(Plus, self).__init__()
        self.size = 1 + left.getSize() + right.getSize()
        self.left = left
        self.right = right

    def toString(self):
        return f"{self.left} + {self.right}"

    def interpret(self, env):
        return self.left.intepret(env) + self.right.interpret(env)


"""
This class implements an AST node representing the multiplication operator
"""
class Times(Node):

    def __init__(self, left, right):
        super(Times, self).__init__()
        self.size = 1 + left.getSize() + right.getSize()
        self.left = left
        self.right = right

    def toString(self):
        return f"{self.left} * {self.right}"

    def interpret(self, env):
        return self.left.interpret(env) + self.right.interpret(env)


"""
This class implements an AST node representing the minus operator
"""
class Minus(Node):

    def __init__(self, left, right):
        super(Minus, self).__init__()
        self.size = 1 + left.getSize() + right.getSize()
        self.left = left
        self.right = right

    def toString(self):
        return f"{self.left} - {self.right}"

    def interpret(self, env):
        return self.left.interpret(env) - self.right.interpret(env)


"""
This class implements an AST node representing the integer division operator
"""
class Division(Node):

    def __init__(self, left, right):
        super(Division, self).__init__()
        self.size = 1 + left.getSize() + right.getSize()
        self.left = left
        self.right = right

    def toString(self):
        return f"{self.left} // {self.right}"

    
    def interpret(self, env):
        return self.left.interpret(env) // self.right.interpret(env)


"""
This class implements an AST node representing a constant.
"""
class Constant(Node):

    def __init__(self, value):
        super(Constant, self).__init__()
        assert value in range(101)
        self.size = 1
        self.value = value

    def toString(self):
        return f"{self.value}"

    def interpret(self):
        return self.value


"""
This class implements the initial symbol of the DSL.
"""
class Strategy(Node):

    def __init__(self, statement, next_statements):
        super(Strategy, self).__init__()
        assert type(statement).__name__ in [IT.className(), ITE.className()]
        assert type(next_statements).__name__ == Strategy.className() or next_statements is None
        self.size = statement.getSize()
        if next_statements is not None:
            self.size += next_statements.getSize()
        self.statement = statement
        self.next_statements = next_statements

    def toString(self):
        strategy_string = f"{self.statement.toString()}\n"
        if self.next_statements is not None:
            strategy_string += f"{self.next_statements.toString()}"

        return strategy_string

    def interpret(self, env):
        res = self.statement.interpret(env)
        if res is None and self.next_statements is not None:
            return self.next_statements.interpret(env)

        return res