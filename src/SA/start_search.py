"""
start_search.py 

Author: Olivier Vadiavaloo

Description:
This module implements the driver code of the Simulated Annealing synthesizer.

It declares the operators, dsfs, constants and scalars to be used during
the synthesis process, and calls the synthesizer with the desired arguments.

"""
from src.SA.sim_anneal import *
from src.evaluation import *
from src.Utils.logger import *

def start_sa(time_limit, log_file, run_optimizer, game, sa_option):
    grammar = {}
    grammar['operators'] = [Plus, 
                            Minus,
                            Times, 
                            Divide, 
                            LessThan, 
                            GreaterThan, 
                            EqualTo, 
                            IT, 
                            ITE, 
                            Strategy, 
                            ReturnAction
                        ]

    grammar['dsfs'] = [NonPlayerObjectPosition, NonPlayerObjectApproaching, PlayerPosition]
    grammar['constants'] = np.arange(0, 101, 0.01).tolist()
    grammar['scalars'] = ['paddle_width']
    grammar['arrays'] = ['actions']
    grammar['array_indexes'] = [0, 1, 2]

    logger = Logger(
        log_file,
        'Simulated Annealing',
        {**run_optimizer, **{'time': time_limit}}
    )
    sa = SimulatedAnnealing(time_limit, logger, run_optimizer)

    eval_funct = Evaluation(0, game)
    sa.synthesize(grammar, 2000, 1, eval_funct, option=sa_option)