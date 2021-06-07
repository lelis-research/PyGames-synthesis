"""
start_search.py 

Author: Olivier Vadiavaloo

Description:
This module implements the driver code of the BUS synthesizer.

It declares the operators, dsfs, constants and scalars to be used during
the synthesis process, and calls the synthesizer with the desired arguments.

"""

from src.BUS.bus import BUS
from src.BUS.bus_dsl import *
from src.evaluation import *

if __name__ == '__main__':

    bus = BUS()

    # Initialize the evaluation object
    eval_funct = Evaluation(0)
    
    # Initialize the arguments to the synthesizer
    operators = [IT, ITE, Strategy, ReturnAction, Plus, Times, Divide, Minus, 
        GreaterThan, LessThan, EqualTo]
    dsfs = [FallingFruitPosition, PlayerPosition]
    constants = [Constant.new(0), Constant.new(1), Constant.new(2), Constant.new(0.5), Constant.new(0.3)]
    scalars = [VarScalar.new('paddle_width'), VarFromArray.new('actions', Constant.new(0)), 
        VarFromArray.new('actions', Constant.new(1)), VarFromArray.new('actions', Constant.new(2))]

    time, program = bus.synthesize(20, operators, constants, scalars, dsfs, eval_funct)
    print("Ran BUS for", time, "seconds\n")
    print("BUS returned the following strategy:\n")
    print(program.to_string())