"""
DSL.py 

Author: Olivier Vadiavaloo

Description:
This module implements the nodes used to create Abstract-Syntax Trees (ASTs)
that represent programs written in the DSL designed for playing the Catcher game.

"""
from pygame.constants import K_w, K_s, K_a, K_d
import numpy as np

import random

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