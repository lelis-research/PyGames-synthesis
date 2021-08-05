"""
start_search.py

Author: Olivier Vadiavaloo

Description:
This module provides the implementation of the driver code for the probe
synthesizer. It creates the list of rules, the pcfg, the logger object
and the probe object.
"""
from math import log10, floor
from src.dsl import *
from src.PROBE.rule import *
from src.PROBE.probe import *
from src.Utils.logger import Logger
from src.Evaluation.evaluation import *

def start_probe(time_limit, log_file, is_parallel, game):

    rules = [
        const_rule,
        var_arr_rule,
        var_from_arr_rule,
        var_scalar_rule,
        non_player_pos_rule,
        non_player_dir_rule,
        player_pos_rule,
        for_each_rule,
        ite_rule,
        it_rule,
        strategy_rule,
        ra_rule,
        plus_rule,
        minus_rule,
        times_rule,
        divide_rule,
        gt_rule,
        lt_rule,
        eq_rule
    ]
    
    uniform_prob = 1 / len(rules)
    uniform_cost = floor(-1 * log10(uniform_prob))

    pcfg = {}

    for rule in rules:
        pcfg[rule] = {probability_key: uniform_prob, cost_key: uniform_cost}

    pcfg['dsfs'] = [NonPlayerObjectPosition, NonPlayerObjectApproaching, PlayerPosition]
    pcfg['constants'] = [0.5, 2]
    pcfg['scalars'] = [
        VarArray.new('actions'),
        VarScalar.new('paddle_width'),
        VarFromArray.new('actions', 0),
        VarFromArray.new('actions', 1),
        VarFromArray.new('actions', 2)
    ]

    eval_factory = EvaluationFactory(0, 10, False, 'NORMAL')
    eval_funct = eval_factory.get_eval_fun(game)

    logger = Logger(
        log_file,
        'PROBE (Guided Bottom-Up Search)',
        {'time': time_limit}
    )

    synthesizer = Probe()
    synthesizer.probe(pcfg, rules, eval_funct, time_limit, logger, is_parallel)