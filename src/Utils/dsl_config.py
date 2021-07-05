"""
dsl_config.py

Author: Olivier Vadiaval

Description:
This module implements the class that will load a game's dsl
from a json config file.
"""
import json
import os
from src.dsl import *

class DslConfig:

    def __init__(self, config_filepath):
        if not os.path.exists(config_filepath):
            raise Exception('Path to config file is invalid')
        
        self.config_filepath =  config_filepath

    def get_grammar(self, game):
        with open(self.config_filepath) as config_f:
            dsl_dict = json.load(config_f)

            grammar = {}
            grammar['dsfs'] = []
            for dsf in dsl_dict[game]['dsfs']:
                grammar['dsfs'].append(Node.get_class(dsf))

            grammar['operators'] = []
            for op in dsl_dict['operators']:
                grammar['operators'].append(Node.get_class(op))

            grammar['scalars'] = dsl_dict['scalars']
            grammar['arrays'] = dsl_dict['arrays']
            grammar['array_indexes'] = dsl_dict[game]['array_indexes']
            grammar['constants'] = np.arange(0, 101, 0.01).tolist()

            return grammar