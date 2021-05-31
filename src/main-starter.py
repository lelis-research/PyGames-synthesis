"""
main-starter.py 

Author: Olivier Vadiavaloo

Description:
This module implements the driver code of the synthesizer.

It declares the operators, dsfs, constants and scalars to be used during
the synthesis process, and calls the synthesizer with the desired arguments.

"""

from src.BUS import BUS
from src.DSL import *
from src.Evaluation import *

if __name__ == '__main__':

    bus = BUS()

    # Initialize the evaluation object
    eval_funct = Evaluation()
    
    # Initialize the arguments to the synthesizer
    operators = [IT, ITE, Strategy, Plus, Times, Divide, Minus, 
        GreaterThan, LessThan, EqualTo]
    dsfs = [FallingFruitPosition, PlayerPosition]
    constants = [Constant(0), Constant(1), Constant(2)]
    scalars = [VarScalar, VarFromArray]

    time, program = bus.synthesize(10, operators, constants, scalars, dsfs, eval_funct)
    print("Ran BUS for", time, "seconds\n")
    print("BUS returned the following strategy:\n")
    print(program.toString())