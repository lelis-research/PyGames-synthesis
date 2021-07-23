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
from src.Evaluation.evaluation import *
from src.Utils.logger import *
import random

def start_bus(time_limit, log_file, score_threshold, run_optimizer, game):

    logger = Logger(
        log_file,
        'Bottom-Up Search (BUS)',
        {**run_optimizer, **{'time': time_limit}}
    )

    bus = BUS(time_limit, logger, run_optimizer)

    # Initialize the evaluation object
    eval_factory = EvaluationFactory(0, 10, False, 'NORMAL')
    eval_funct = eval_factory.get_eval_fun(game)
    
    # Initialize the arguments to the synthesizer
    operators = [ForEach, IT, ITE, Strategy, ReturnAction, Plus, Times, Divide, Minus, 
        GreaterThan, LessThan, EqualTo]
    dsfs = [NonPlayerObjectPosition, NonPlayerObjectApproaching, PlayerPosition]
    # constants = np.arange(0, 101, 0.01).tolist()
    constants = [round(random.uniform(0, 101), 2), round(random.uniform(0, 101), 2)]
    scalars = [
        VarArray.new('actions'),
        VarScalar.new('paddle_width'),
        VarFromArray.new('actions', 0),
        VarFromArray.new('actions', 1),
        VarFromArray.new('actions', 2)
    ]

    bus.synthesize(30, operators, constants, scalars, dsfs, eval_funct)