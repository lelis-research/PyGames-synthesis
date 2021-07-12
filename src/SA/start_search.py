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
from src.Utils.dsl_config import *
import json

def start_sa(time_limit, log_file, run_optimizer, game,
    sa_option, verbose, plot, save, plot_filename, ibr, total_games):
    if ibr:
        assert available_games[game] == 2, f'Cannot perform IBR on {game}'

    dsl_config = DslConfig('./src/dsl_config.json')
    grammar = dsl_config.get_grammar(game)

    logger = Logger(
        log_file,
        'Simulated Annealing',
        {**run_optimizer, **{'time': time_limit}}
    )
    sa = SimulatedAnnealing(time_limit, logger, run_optimizer)

    eval_factory = EvaluationFactory(0, total_games)
    eval_funct = eval_factory.get_eval_fun(game)
    
    sa.synthesize(
        grammar, 
        2000, 
        1, 
        eval_funct,
        plot_filename, 
        ibr,
        option=sa_option,
        verbose_opt=verbose, 
        generate_plot=plot,
        save_data=save
    )