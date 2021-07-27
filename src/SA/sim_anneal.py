"""
sim_anneal.py

Author: Olivier Vadiavaloo

Description:
This file contains the code implementing the simulated annealing
algorithm.

"""
import copy as cp
from time import time
import random
import multiprocessing as mp
from math import exp
from src.dsl import *
from src.Evaluation.evaluation import *
from src.Optimizer.optimizer import *
from src.SA.plotter import *
from statistics import *

class SimulatedAnnealing:

    def __init__(self, time_limit, logger, run_optimizer):
        self.time_limit = time_limit
        self.is_triage = run_optimizer['triage']
        self.run_optimizer = run_optimizer['run_optimizer']
        self.n_iter = run_optimizer['iterations']
        self.kappa = run_optimizer['kappa']
        self.opt_is_parallel = run_optimizer['parallel']
        self.logger = logger

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

    def complete_program(self, p, depth, max_depth, max_size):
        if not isinstance(p, Node):
            return

        for i in range(p.get_max_number_children()):
            valid_ith_child_types = p.get_valid_children_types()[i]

            # if p is a scalar or constant, no need to call complete_program on child
            if isinstance(p, VarScalar) or isinstance(p, VarFromArray) or \
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

    def generate_random(self):
        while True:
            initial_nodes = Node.get_valid_children_types()[0]
            random_p = Node.instance(random.choice(list(initial_nodes)))
            self.complete_program(random_p, self.initial_depth, self.max_depth, self.max_size)
            random_p.check_correct_size()

            if self.closed_list.get(random_p.to_string()) is None:
                return random_p

    def mutate_inner_nodes(self, p, index):
        self.processed_nodes += 1

        if not isinstance(p, Node):
            return False

        for i in range(p.get_max_number_children()):

            if index == self.processed_nodes:
                valid_ith_child_types = p.get_valid_children_types()[i]
                
                child = Node.instance(random.choice(list(valid_ith_child_types)))

                if isinstance(child, Node):
                    self.complete_program(child, self.initial_depth, self.max_depth, self.max_size-p.get_size())
                p.replace_child(child, i)

                return True

            if self.mutate_inner_nodes(p.get_children()[i], index):
                return True

        return False

    def mutate(self, p):
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
                if self.closed_list.get(p.to_string()) is None:
                    return p

            self.processed_nodes = 0
            self.mutate_inner_nodes(p, index)
            p.check_correct_size()

            # Check for duplicates
            if self.closed_list.get(p.to_string()) is None:
                return p

    def reduce_temp(self, current_t, epoch):
        return current_t / (1 + self.alpha * epoch)

    def is_accept(self, j_diff, temp):
        rand = random.uniform(0, 1)
        if rand < min(1, exp(j_diff * (self.beta / temp))):
            return True
        return False

    def check_new_best(self, candidate, candidate_eval, best_eval, eval_funct):
        if candidate_eval > best_eval:
            
            if candidate_eval > eval_funct.STRONG_SCORE:
                print('before run longer', candidate_eval)
                more_accurate_eval = self.run_longer_eval(eval_funct, candidate)
                print('after run longer', candidate_eval)

                if more_accurate_eval > best_eval:
                    return True, more_accurate_eval
                else:
                    return False, more_accurate_eval

            return True, candidate_eval

        return False, candidate_eval

    def init_var_child_types(self, grammar):
        VarArray.valid_children_types = [set(grammar['arrays'])]
        VarFromArray.valid_children_types = [set(grammar['arrays']), set(grammar['array_indexes'])]
        VarScalar.valid_children_types = [set(grammar['scalars'])]
        Constant.valid_children_types = [set(grammar['constants'])]

    def init_attributes(self, eval_funct):
        self.alpha = 0.9
        self.beta = 100
        self.initial_depth = 0
        self.max_depth = 4
        self.max_size = 50
        self.ppool = []     # for storing solutions to be optimized

        if self.opt_is_parallel:
            # Change this number to change the number of
            # solutions to be optimized in parallel
            self.ppool_max_size = 5
        else:
            self.ppool_max_size = 1

        # Initialize variables used to generate plots later on
        self.scores_dict = {}
        self.best_pscore_dict = {}
        self.optimized_pscore_dict = {}
        self.unoptimized_pscore_dict = {}

        # Declare optimizer if command-line option was specified
        if self.run_optimizer:
            self.optimizer = Optimizer(eval_funct, self.is_triage, self.n_iter, self.kappa)

    def start_optimizer(self, verbose=False):
        if self.opt_is_parallel:
            with mp.Pool() as pool:
                current_best = None
                current_best_score = Evaluation.MIN_SCORE
                current_best_is_optimized = False
                for arg, res in zip(self.ppool, pool.starmap(self.optimizer.optimize, self.ppool, chunksize=20)):
                    optimized_p, optimized_const_values, new_score, is_optimized = res
                    arg_p, arg_pscore = arg

                    if is_optimized and verbose:
                        pdescr = {
                            'header': 'Optimized Program', 
                            'psize': optimized_p.get_size(), 
                            'score': new_score,
                            'timestamp': self.get_timestamp()
                            }
                        self.logger.log('Constant Values: ' + str(optimized_const_values))
                        self.logger.log_program(optimized_p.to_string(indent=1), pdescr)
                        self.logger.log('Previous Score: ' + str(arg_pscore), end='\n\n')
                        
                    if new_score > current_best_score:
                        current_best_score = new_score
                        current_best = optimized_p
                        current_best_is_optimized = is_optimized

                return current_best, current_best_score, current_best_is_optimized

        else:
            p, pscore = self.ppool[0]
            optimized_p, optimized_const_values, new_score, is_optimized = self.optimizer.optimize(p, pscore)
            
            if is_optimized and verbose:
                pdescr = {'header': 'Optimized Program', 'psize': optimized_p.get_size(), 'score': new_score}
                self.logger.log_program(optimized_p.to_string(indent=1), pdescr)
                self.logger.log('Constant Values: ' + str(optimized_const_values))
                self.logger.log('Previous Score: ' + str(pscore), end='\n\n')
            
            return optimized_p, new_score, is_optimized

    def get_timestamp(self):
        return round((time() - self.start) / 60, 2)

    def synthesize(
            self,
            grammar, 
            current_t, 
            final_t, 
            eval_funct, 
            plot_filename,
            ibr,
            option=1, 
            verbose_opt=False, 
            generate_plot=False,
            save_data=False
        ):
        """
        This method implements the simulated annealing algorithm that can be used
        to generate strategies given a grammar and an evaluation function.

            - CFG: grammar
            - current_t: initial temperature
            - final_t: final temperature
            - option: 1 or 2
                -- Option 1: Does not generate a random program each time simulated annealing
                             finishes to run. More likely to get stuck on a local min/max.
                -- Option 2: Generates a random program after each simulated annealing run.

        """
        self.start = time()

        self.init_var_child_types(grammar)
        self.init_attributes(eval_funct)

        initial_t = current_t
        iterations = 0
        self.closed_list = {}

        # Option 2: Generate random program only once
        if option == 2:
            best = self.generate_random()
            timestamp = self.get_timestamp()
            scores, best_eval = eval_funct.evaluate(best, verbose=True)
            self.closed_list[best.to_string()] = (best_eval, timestamp)

            eval_funct.set_best(best, best_eval)    # update best score in eval object

            # Set baseline for optimizer
            if self.run_optimizer:
                    self.optimizer.set_baseline_eval(best_eval)

            self.best_pscore_dict[iterations] = (best_eval, timestamp)

        else:
            best = None
            best_eval = None

        '''
        Run Simulated Annealing until time limit is reached
        If option 1 is specified, generate a random program for
        the initial program. If option 2 is specified, use best
        as the initial program.
        '''
        while time() - self.start < self.time_limit:
            current_t = initial_t
            timestamp = self.get_timestamp()

            # Option 1: Generate random program and compare with best
            if option == 1:
                current = self.generate_random()
                scores, current_eval = eval_funct.evaluate(current, verbose=True)
                self.closed_list[current.to_string()] = (current_eval, timestamp)   # save to closed_list

                if best is not None:
                    new_best, current_eval = self.check_new_best(current, current_eval, best_eval, eval_funct)

                if best is None or new_best:
                    best, best_eval = current, current_eval
                    eval_funct.set_best(best, best_eval)        # update best score in eval object

                    # Set baseline for optimizer
                    if self.run_optimizer:
                        self.optimizer.set_baseline_eval(best_eval)

                    self.best_pscore_dict[iterations] = (best_eval, timestamp)
            
            # Option 2: Assign current to best solution in previous iteration
            elif option == 2 and best is not None:
                current = best
                current_eval = best_eval

            if verbose_opt:
                # Log initial program to file
                pdescr = {
                            'header': 'Initial Program',
                            'psize': current.get_size(), 
                            'score': current_eval,
                            'timestamp': timestamp
                        }
                self.logger.log_program(current.to_string(), pdescr)
                self.logger.log('Scores: ' + str(scores).strip('()'), end='\n\n')

            if current_eval != Evaluation.MIN_SCORE:
                self.scores_dict[iterations] = (current_eval, timestamp)

            iterations += 1

            # Call simulated annealing
            best, best_eval, epochs = self.simulated_annealing(
                                current_t,
                                final_t,
                                current,
                                best,
                                current_eval,
                                best_eval,
                                iterations,
                                eval_funct,
                                verbose_opt,
                                ibr
                            )

            iterations += epochs

        self.logger.log('Running Time: ' + str(round(time() - self.start, 2)) + 'seconds')
        self.logger.log('Iterations: ' + str(iterations), end='\n\n')

        # Log best program
        pdescr = {
                'header': 'Best Program Found By SA',
                'psize': best.get_size(), 
                'score': best_eval,
                'timestamp': self.closed_list[best.to_string()][1]
            }
        self.logger.log_program(best.to_string(), pdescr)

        # Plot data if required
        if generate_plot:
            self.plot(plot_filename)

        # Save data
        if save_data:
            self.save(plot_filename)

        return best, best_eval

    def save(self, plot_filename):
        plotter = Plotter()
        data_filenames_dict = plotter.construct_dat_filenames(plot_filename)

        # Bundle values of dict into a list
        data_filenames = []
        data_filenames.extend(list(data_filenames_dict.values()))

        if self.run_optimizer:
            plotter.save_data(
                self.scores_dict, 
                self.best_pscore_dict, 
                self.unoptimized_pscore_dict,
                self.optimized_pscore_dict,
                names=data_filenames
            )

        else:
            plotter.save_data(
                self.scores_dict, 
                self.best_pscore_dict,
                names=data_filenames
            )

    def plot(self, plot_filename):
        plotter = Plotter()     # Plotter object
        plot_names = {
            'x': 'Iterations',
            'y': 'Program Score',
            'z': 'Iterations',
            'title': 'SA Program Scores vs Total Iterations',
            'filename': plot_filename,
            'legend': ['current program', 'best program', 'unoptimized program']
        }

        plotter.plot_from_data(self.scores_dict, self.best_pscore_dict, names=plot_names)     # plot all scores

    def run_longer_eval(self, eval_funct, program):
        # Change the evaluation object's configuration
        new_config_attributes = form_basic_attr_dict(
                                    False,
                                    50,
                                    eval_funct.get_best()[1],
                                    eval_funct.MIN_SCORE,
                                    None
                                )

        original_eval_config = eval_funct.change_config("NORMAL", new_config_attributes)
        program_eval = eval_funct.evaluate_parallel(program, verbose=False)
        eval_funct.set_config(original_eval_config)

        return program_eval

    def simulated_annealing(
            self,
            current_t,
            final_t,
            current,
            best,
            current_eval,
            best_eval,
            iterations,
            eval_funct,
            verbose_opt,
            ibr
        ):
        epoch = 0
        mutations = 0
        while current_t > final_t:
            best_updated = False
            header = 'Mutated Program'
            timestamp = self.get_timestamp()

            # Mutate current program
            candidate = self.mutate(cp.deepcopy(current))
            mutations += 1

            # Evaluate the mutated program
            scores, candidate_eval = eval_funct.evaluate(candidate, verbose=True)

            # Run optimizer if flag was specified
            if self.run_optimizer:
                self.ppool.append((candidate, candidate_eval))
                # print('self.ppool_len', len(self.ppool))

                if len(self.ppool) >= self.ppool_max_size:
                    unoptimized_candidate_eval = candidate_eval
                    candidate, candidate_eval, is_optimized = self.start_optimizer()

                    # Store optimized candidates into closed_list
                    if is_optimized:
                        self.unoptimized_pscore_dict[iterations + epoch] = (unoptimized_candidate_eval, timestamp)
                        self.optimized_pscore_dict[iterations + epoch] = (candidate_eval, timestamp)

                    self.ppool = []

            new_best, candidate_eval = self.check_new_best(candidate, candidate_eval, best_eval, eval_funct)
            
            if new_best:
                header = 'New Best Program'
                best_updated = True
                best, best_eval = candidate, candidate_eval

                # Set the best program and its score in eval_funct
                # Since triage is used, the best score in eval_funct must be updated
                eval_funct.set_best(best, best_eval)

                # Update the baseline score of the optimizer
                if self.run_optimizer:
                    self.optimizer.set_baseline_eval(best_eval)
                
                self.best_pscore_dict[iterations + epoch] = (best_eval, timestamp)

            # If candidate program does not raise an error, store scores
            if candidate_eval != Evaluation.MIN_SCORE:  
                self.scores_dict[iterations + epoch] = (candidate_eval, timestamp)

            self.closed_list[candidate.to_string()] = (candidate_eval, timestamp)

            # Log program to file
            if best_updated or verbose_opt:
                pdescr = {
                        'header': header, 
                        'psize': candidate.get_size(), 
                        'score': candidate_eval,
                        'timestamp': timestamp
                    }
                self.logger.log_program(candidate.to_string(), pdescr)
                self.logger.log('Scores: ' + str(scores).strip('()'))
                self.logger.log('Mutations: ' + str(mutations), end='\n\n')

            j_diff = candidate_eval - current_eval
            
            # Decide whether to accept the candidate program
            if j_diff > 0 or self.is_accept(j_diff, current_t):
                current, current_eval = candidate, candidate_eval
            
            current_t = self.reduce_temp(current_t, epoch)
            epoch += 1

            # If using IBR, break out of loop once a best response is found
            if ibr and best_updated:
                break

        return best, best_eval, epoch+1