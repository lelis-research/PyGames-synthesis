"""
program_mutator.py

Author: Olivier Vadiavaloo

Description:
This file contains the implementation of the ProgramGenerator class, whose
responsibility is to generate and/or mutate programs.
"""
from src.dsl import *
import random

class ProgramMutator:

    def __init__(self, initial_depth, max_depth, max_size):
        self.initial_depth = initial_depth
        self.max_depth = max_depth
        self.max_size = max_size

    def generate_random(self, closed_list):
        while True:
            initial_nodes = Node.get_valid_children_types()[0]
            random_p = Node.instance(random.choice(list(initial_nodes)))
            self.complete_program(random_p, self.initial_depth, self.max_depth, self.max_size)
            random_p.check_correct_size()

            if closed_list.get(random_p.to_string()) is None:
                return random_p

    def complete_program(self, p, depth, max_depth, max_size):
        if not isinstance(p, Node):
            return

        for i in range(p.get_max_number_children()):
            valid_ith_child_types = p.get_valid_children_types()[i]

            if isinstance(p, ReturnAction):
                action_index = random.choice(list(valid_ith_child_types))
                child = VarFromArray.new('actions', action_index)
                p.add_child(child)

            # if p is a scalar or constant, no need to call complete_program on child
            elif isinstance(p, VarScalar) or isinstance(p, VarFromArray) or \
                isinstance(p, Constant) or isinstance(p, VarArray):
                child = random.choice(list(valid_ith_child_types))
                p.add_child(child)

            # if max depth is exceeded, get a terminal node
            elif depth >= max_depth or p.get_size() >= max_size:
                child = self.get_terminal_node(p, valid_ith_child_types)
                p.add_child(child)
                self.complete_program(child, depth+1, max_depth, max_size)

            # else choose a random child node
            else:
                child = Node.instance(random.choice(list(valid_ith_child_types)))
                p.add_child(child)
                self.complete_program(child, depth+1, max_depth, max_size)

    def get_terminal_node(self, p, valid_ith_child_types):
        terminal_nodes = []

        for child_type in valid_ith_child_types:
            if child_type is None or type(child_type) is int:
                terminal_nodes.append(child_type)
                continue

            child = Node.instance(child_type)
            if child_type in [VarFromArray.className(), VarArray.className(), VarScalar.className(), Constant.className()] \
                or child.get_max_number_children() == 0:
                terminal_nodes.append(child)

        if terminal_nodes == 0:
            for child_type in valid_ith_child_types:
                child = Node.instance(child_type)

                if child.get_max_children_number() == 1:
                    terminal_nodes.append(child)

        if len(terminal_nodes) > 0:
            return random.choice(terminal_nodes)

        return Node.instance(random.choice(list(valid_ith_child_types)))

    def mutate_inner_nodes(self, p, index):
        self.processed_nodes += 1

        if not isinstance(p, Node):
            return False

        for i in range(p.get_max_number_children()):

            if index == self.processed_nodes:
                valid_ith_child_types = p.get_valid_children_types()[i]
                
                child = Node.instance(random.choice(list(valid_ith_child_types)))
                if isinstance(p, ReturnAction):
                    child = VarFromArray.new('actions', child)

                elif isinstance(child, Node):
                    self.complete_program(child, self.initial_depth, self.max_depth, self.max_size-p.get_size())
                p.replace_child(child, i)

                return True

            if self.mutate_inner_nodes(p.get_children()[i], index):
                return True

        return False

    def mutate(self, p, closed_list):
        while True:
            # print('p.get_size()', p.get_size())
            index = random.randint(0, p.get_size())
            # print('index', index)
            # print()

            # root will be mutated
            if index == 0:
                ptypes = Node.get_valid_children_types()[0]
                p = Node.instance(random.choice(list(ptypes)))
                self.complete_program(p, self.initial_depth, self.max_depth, self.max_size)
                p.check_correct_size()

                # Check for duplicates
                if closed_list.get(p.to_string()) is None:
                    return p

            self.processed_nodes = 0
            self.mutate_inner_nodes(p, index)
            p.check_correct_size()

            # Check for duplicates
            if closed_list.get(p.to_string()) is None:
                return p