"""
dsl.py 

Author: Olivier Vadiavaloo

Description:
This module implements the nodes used to create Abstract-Syntax Trees (ASTs)
that represent programs written in the DSL designed for playing games implemented
in the PyGame-Learning-Environment.

"""
from random import choice
from pygame.constants import K_w, K_s, K_a, K_d
import numpy as np

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
        self.loopname = 'loop'

    def add_child(self, child):
        if type(self).__name__ == Constant.className():
            assert type(child).__name__ != Constant.className()

        assert len(self.children) < self.max_number_children
        self.children.append(child)
        self.current_child_num += 1
        
        if isinstance(child, Node):
            self.size += child.get_size()
        elif child is not None:
            self.size += 1

    def replace_child(self, child, i):
        if type(self).__name__ == Constant.className():
            assert type(child).__name__ != Constant.className()
        
        if isinstance(self.children[i], Node):
            self.size -= self.children[i].get_size()
        elif self.children[i] is not None:
            self.size -= 1

        if isinstance(child, Node):
            self.size += child.get_size()
        elif child is not None:
            self.size += 1

        self.children[i] = child

    def check_correct_size(self):
        size_zero_nodes = set([
                            Strategy.className(),
                            Constant.className(),
                            VarScalar.className(),
                            VarFromArray.className()
        ])
        
        if type(self).__name__ in size_zero_nodes:
            size = 0
        else:
            size = 1
        
        for child in self.get_children():
            if isinstance(child, Node):
                child_size = child.check_correct_size()
            else:
                child_size = 1
            size += child_size

        if size != self.get_size():
            self.size = size
        
        return self.size

    def get_size(self):
        return self.size

    def to_string(self, indent=0):
        raise Exception("Unimplemented method: to_string")

    def interpret(self):
        raise Exception("Unimplemented method: interpret")

    def get_children(self):
        return self.children.copy()

    def get_current_child_num(self):
        return self.current_child_num

    def get_max_number_children(self):
        return self.max_number_children

    @staticmethod
    def instance(classname):
        if classname in globals():
            return globals()[classname]()
        return classname

    @staticmethod
    def get_class(classname):
        if classname in globals():
            return globals()[classname]
        else:
            raise Exception(f'Invalid classname: {classname}')

    @classmethod
    def get_valid_children_types(cls):
        return cls.valid_children_types.copy()

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
        self.max_number_children = 1
        self.size = 0

    @classmethod
    def new(cls, value):
        assert value in np.arange(0, 101, 0.01)
        inst = cls()
        inst.add_child(value)
        
        return inst

    def to_string(self, indent=0):
        return f"{self.get_children()[0]}"

    def interpret(self, env):
        return self.get_children()[0]


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

    def to_string(self, indent=0):
        tab = ''
        for _ in range(indent):
            tab += '\t'
        
        action = self.get_children()[0]
        return f"{tab}return {action.to_string()}"

    def interpret(self, env):
        action = self.get_children()[0]
        return action.interpret(env)

"""
This class represents a for loop in the DSL. It is interpreted as
a for-each loop where the program iterates over each element of the
provided iterable directly. For example,

for each x in coords:
    # loop body
"""
class ForEach(Node):

    def __init__(self):
        super(ForEach, self).__init__()
        self.max_number_children = 2

    @classmethod
    def new(cls, iterable, loop_body):
        assert isinstance(iterable, VarArray)
        assert isinstance(loop_body, IT) or isinstance(loop_body, ITE)
        inst = cls()
        inst.add_child(iterable)
        inst.add_child(loop_body)

        return inst

    def to_string(self, indent=0):
        tabs = ''
        for _ in range(indent):
            tabs += '\t'

        iterable = self.get_children()[0]
        loop_body = self.get_children()[1]
        for_str = f"""{tabs}for each element in {iterable.to_string()}:\n"""
        for_str += loop_body.to_string(indent+1)

        return for_str

    def interpret(self, env):
        iterable = self.get_children()[0]
        loop_body = self.get_children()[1]

        for element in iterable.interpret(env):
            env[self.loopname] = element
            loop_res = loop_body.interpret(env)
            
            if loop_res != 'False':
                env[self.loopname] = None
                return loop_res

        env[self.loopname] = None


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
        assert type(if_body).__name__ in [ReturnAction.className(), IT.className()]
        inst = cls()
        inst.add_child(condition)
        inst.add_child(if_body)

        return inst

    def to_string(self, indent=0):
        tab = ""
        for _ in range(indent):
            tab += "\t"

        condition = self.get_children()[0]
        if_body = self.get_children()[1]
        
        it_string = f"""{tab}if {condition.to_string()}:\n"""
        it_string += f"""{if_body.to_string(indent+1)}"""
        return it_string

    def interpret(self, env):
        condition = self.get_children()[0]
        if_body = self.get_children()[1]

        if condition.interpret(env):
            return if_body.interpret(env)

        if env.get(self.loopname) is not None:
            return 'False'
    

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

    def to_string(self, indent=0):
        tab = ""
        for _ in range(indent):
            tab += "\t"
        
        condition = self.get_children()[0]
        if_body = self.get_children()[1]
        else_body = self.get_children()[2]

        ite_string = f"""{tab}if {condition.to_string()}:\n"""
        ite_string += f"""{if_body.to_string(indent+1)}\n"""
        ite_string += f"""{tab}else:\n"""
        ite_string += f"""{else_body.to_string(indent+1)}"""
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

    def to_string(self, indent=0):
        return PlayerPosition.className()

    def interpret(self, env):
        return env[self.statename]['player_position']


"""
This class implements a domain-specific function that returns
the x-position of the non-player object. The non-player object
is the falling fruit in the Catcher game, while in Pong, it is
the ball.
"""
class NonPlayerObjectPosition(Node):

    def __init__(self):
        super(NonPlayerObjectPosition, self).__init__()
        self.max_number_children = 0

    def to_string(self, indent=0):
        return NonPlayerObjectPosition.className()

    def interpret(self, env):
        return env[self.statename]['non_player_position']


"""
This class implements a DSF that returns True if the non-player
object is moving towards the player and False otherwise.
"""
class NonPlayerObjectApproaching(Node):
    
    def __init__(self):
        super(NonPlayerObjectApproaching, self).__init__()
        self.max_number_children = 0

    def to_string(self, indent=0):
        return NonPlayerObjectApproaching.className()

    def interpret(self, env):
        return env[self.statename]['non_player_approaching']


"""
This class implements an AST node representing a domain-specific scalar variable.
For instance, the player's paddle width.
"""
class VarScalar(Node):

    def __init__(self):
        super(VarScalar, self).__init__()
        self.max_number_children = 1
        self.size = 0

    @classmethod
    def new(cls, name):
        inst = cls()
        inst.add_child(name)

        return inst

    def to_string(self, indent=0):
        return f"{self.get_children()[0]}"

    def interpret(self, env):
        return env[self.get_children()[0]]


"""
This class implements an AST node represent a list variable
"""
class VarArray(Node):

    def __init__(self):
        super(VarArray, self).__init__()
        self.max_number_children = 1
        self.size = 0

    @classmethod
    def new(cls, array_name):
        assert type(array_name) is str
        inst = cls()
        inst.add_child(array_name)

        return inst

    def to_string(self, indent=0):
        array_name = self.get_children()[0]
        assert type(array_name) is str
        return array_name

    def interpret(self, env):
        array_name = self.get_children()[0]
        return env[array_name]


"""
This class implements an AST node representing a domain-specific variable from
an array. For example, actions[0]
"""
class VarFromArray(Node):

    def __init__(self):
        super(VarFromArray, self).__init__()
        self.max_number_children = 2
        self.size = 0

    @classmethod
    def new(cls, name, index):
        inst = cls()
        inst.add_child(name)
        inst.add_child(index)

        return inst
    
    def to_string(self, indent=0):
        name = self.get_children()[0]
        index = self.get_children()[1]
        if isinstance(index, Node) or type(index).__name__ == Constant.className():
            index = index.to_string()
        
        return f"{name}[{index}]"

    def interpret(self, env):
        name = self.get_children()[0]
        index = self.get_children()[1]
        if isinstance(index, Node) or type(index).__name__ == Constant.className():
            index = index.interpret(env)

        return env[name][index]


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

    def to_string(self, indent=0):
        return f"{self.get_children()[0].to_string()} < {self.get_children()[1].to_string()}"

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

    def to_string(self, indent=0):
        return f"{self.get_children()[0].to_string()} > {self.get_children()[1].to_string()}"

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

    def to_string(self, indent=0):
        return f"{self.get_children()[0].to_string()} == {self.get_children()[1].to_string()}"

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

    def to_string(self, indent=0):
        return f"({self.get_children()[0].to_string()} + {self.get_children()[1].to_string()})"

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

    def to_string(self, indent=0):
        return f"({self.get_children()[0].to_string()} * {self.get_children()[1].to_string()})"

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

    def to_string(self, indent=0):
        return f"({self.get_children()[0].to_string()} - {self.get_children()[1].to_string()})"

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

    def to_string(self, indent=0):
        return f"({self.get_children()[0].to_string()} // {self.get_children()[1].to_string()})"

    
    def interpret(self, env):
        return self.get_children()[0].interpret(env) // self.get_children()[1].interpret(env)


"""
This class implements the initial symbol of the DSL.
"""
class Strategy(Node):

    def __init__(self):
        super(Strategy, self).__init__()
        self.size = 0
        self.max_number_children = 2

    @classmethod
    def new(cls, statement, next_statements):
        assert type(statement).__name__ in [IT.className()]
        assert type(next_statements).__name__ in [Strategy.className(), ReturnAction.className(), type(None).__name__]

        if type(statement).__name__ == ITE.className():
            next_statements = None
        
        inst = cls()
        inst.add_child(statement)
        inst.add_child(next_statements)

        return inst

    def to_string(self, indent=0):
        statement = self.get_children()[0]
        next_statements = self.get_children()[1]

        strategy_string = f"{statement.to_string(indent)}\n"
        if next_statements is not None:
            strategy_string += f"{next_statements.to_string(indent)}"

        return strategy_string

    def interpret(self, env):
        statement = self.get_children()[0]
        next_statements = self.get_children()[1]

        res = statement.interpret(env)
        if res is None and next_statements is not None:
            return next_statements.interpret(env)

        return res


Node.valid_children_types = [set([Strategy.className(), ITE.className()])]

Strategy.valid_first_statement = set([IT.className()])
Strategy.valid_next_statements = set([Strategy.className(), ReturnAction.className(), None])
Strategy.valid_children_types = [Strategy.valid_first_statement, Strategy.valid_next_statements]

ForEach.valid_iterable = set([VarArray.className()])
ForEach.valid_loop_body = set([IT.className(), ITE.className()])
ForEach.valid_children_types = [ForEach.valid_iterable, ForEach.valid_loop_body]

IT.valid_if_cond = set([LessThan.className(), GreaterThan.className(), EqualTo.className(), NonPlayerObjectApproaching.className()])
IT.valid_if_body = set([ReturnAction.className(), IT.className()])
IT.valid_children_types = [IT.valid_if_cond, IT.valid_if_body]

ITE.valid_if_cond = IT.valid_if_cond
ITE.valid_if_body = set([ReturnAction.className()])
ITE.valid_else_body = set([ReturnAction.className()])
ITE.valid_children_types = [ITE.valid_if_cond, ITE.valid_if_body, ITE.valid_else_body]

ReturnAction.valid_action = set([VarFromArray.className()])
ReturnAction.valid_children_types = [ReturnAction.valid_action]

Plus.valid_operands = set([Constant.className(),
                        VarScalar.className(),
                        NonPlayerObjectPosition.className(),
                        PlayerPosition.className(),
                        Plus.className(),
                        Minus.className(),
                        Divide.className(),
                        Times.className()
                    ])
Plus.valid_children_types = [Plus.valid_operands, Plus.valid_operands]

Minus.valid_operands = Plus.valid_operands.copy()
Minus.valid_children_types = [Minus.valid_operands, Minus.valid_operands]

Times.valid_operands = Plus.valid_operands.copy()
Times.valid_children_types = [Times.valid_operands, Times.valid_operands]

Divide.valid_operands = Plus.valid_operands.copy()
Divide.valid_children_types = [Divide.valid_operands, Divide.valid_operands]

LessThan.valid_operands = set([Constant.className(),
                            VarScalar.className(),
                            NonPlayerObjectPosition.className(),
                            PlayerPosition.className(),
                            Plus.className(),
                            Minus.className(),
                            Times.className(),
                            Divide.className()
                        ])
LessThan.valid_children_types = [LessThan.valid_operands, LessThan.valid_operands]

GreaterThan.valid_operands = LessThan.valid_operands.copy()
GreaterThan.valid_children_types = [GreaterThan.valid_operands, LessThan.valid_operands]

EqualTo.valid_operands = LessThan.valid_operands.copy()
EqualTo.valid_children_types = [EqualTo.valid_operands, EqualTo.valid_operands]