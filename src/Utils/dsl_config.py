"""
dsl_config.py

Author: Olivier Vadiaval

Description:
This module implements the class that will load a game's dsl
from a json config file.
"""
import json
import os
import random
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

            if 'scalars' in dsl_dict[game]:
                grammar['scalars'] = dsl_dict[game]['scalars']
            else:
                grammar['scalars'] = dsl_dict['scalars']

            if 'arrays' in dsl_dict[game]:
                grammar['arrays'] = dsl_dict[game]['arrays']
            else:
                grammar['arrays'] = dsl_dict['arrays']

            if 'array_indexes' in dsl_dict[game]:
                grammar['array_indexes'] = dsl_dict[game]['array_indexes']
            else:
                grammar['array_indexes'] = dsl_dict['array_indexes']

            grammar['constants'] = [random.uniform(-100.01, 100.01)]

            return grammar

    def assign_valid_children_types(
        self,
        node,
        game_specific_children_types,
        valid_children_types
    ):
        node_valid_children = []
                
        if game_specific_children_types is not None and node in game_specific_children_types:
            valid_children_types_lists = game_specific_children_types[node]
        else:
            valid_children_types_lists = valid_children_types[node]

        for children_types_list in valid_children_types_lists:
            if 'None' in children_types_list:
                children_types_list.remove('None')
                children_types_list.append(None)
            
            node_valid_children.append(set(children_types_list))

        return node_valid_children.copy()

    def init_valid_children_types(self, game):
        with open(self.config_filepath) as config_f:
            dsl_dict = json.load(config_f)

            valid_children_types = dsl_dict['valid_children_types']
            game_specific_children_types = dsl_dict[game].get('valid_children_types')

            for node in valid_children_types.keys():
                
                if node in ['arithmetic', 'comparison']:
                    for operator in dsl_dict[node]:
                        Node.get_class(operator).valid_children_types = self.assign_valid_children_types(
                                                        node,
                                                        game_specific_children_types,
                                                        valid_children_types
                                                    )

                else:
                    Node.get_class(node).valid_children_types = self.assign_valid_children_types(
                                                        node,
                                                        game_specific_children_types,
                                                        valid_children_types
                                                    )

            if game_specific_children_types is not None:
                for node in game_specific_children_types.keys():
                    if node not in valid_children_types.keys():
                        Node.get_class(node).valid_children_types = self.assign_valid_children_types(
                                                        node,
                                                        game_specific_children_types,
                                                        valid_children_types
                                                    )