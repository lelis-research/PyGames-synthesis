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
from src.Optimizer.start_optimizer import *
from src.SA.plotter import *
from statistics import *

class SimulatedAnnealing:

    def __init__(self, time_limit, logger, optimizer, program_mutator):
        self.time_limit = time_limit
        self.logger = logger
        if optimizer is None:
            self.run_optimizer = False
        else:
            self.run_optimizer = True
            self.optimizer = optimizer

        self.program_mutator = program_mutator

    def reduce_temp(self, current_t, epoch):
        return current_t / (1 + self.alpha * epoch)

    def is_accept(self, j_diff, temp):
        rand = random.uniform(0, 1)
        if rand < min(1, exp(j_diff * (self.beta / temp))):
            return True
        return False

    def check_new_best(self, candidate, candidate_eval, candidate_scores, best_eval, eval_funct):
        if candidate_eval > best_eval:
            
            if candidate_eval > eval_funct.STRONG_SCORE:
                print('before run longer', candidate_eval)
                more_accurate_scores, more_accurate_eval = self.run_longer_eval(eval_funct, candidate)
                print('after run longer', more_accurate_eval)

                if more_accurate_eval > best_eval:
                    return True, more_accurate_eval, more_accurate_scores
                else:
                    return False, more_accurate_eval, more_accurate_scores

            return True, candidate_eval, candidate_scores

        return False, candidate_eval, candidate_scores

    def init_attributes(self, eval_funct):
        self.alpha = 0.9
        self.beta = 100
        self.ppool = []     # for storing solutions to be optimized

        if self.run_optimizer:
            if self.optimizer.get_parallel():
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

    def get_timestamp(self):
        return round((time() - self.start) / 60, 2)

    def synthesize(
            self,
            current_t, 
            final_t, 
            eval_funct, 
            plot_filename,
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
        self.init_attributes(eval_funct)

        initial_t = current_t
        iterations = 0
        self.closed_list = {}

        # Option 2: Generate random program only once
        if option == 2:
            best = self.program_mutator.generate_random(self.closed_list)
            timestamp = self.get_timestamp()
            scores, best_eval = eval_funct.evaluate(best, verbose=True)
            self.closed_list[best.to_string()] = (best_eval, timestamp)

            eval_funct.set_best(best, best_eval, scores)    # update best score in eval object

            # Set baseline for optimizer
            if self.run_optimizer:
                    self.optimizer.set_baseline_eval(best_eval)

            if best_eval != Evaluation.MIN_SCORE:
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
                current = self.program_mutator.generate_random(self.closed_list)
                scores, current_eval = eval_funct.evaluate(current, verbose=True)
                self.closed_list[current.to_string()] = (current_eval, timestamp)   # save to closed_list

                if best is not None:
                    new_best, current_eval, scores = self.check_new_best(current, current_eval, scores, best_eval, eval_funct)

                if best is None or new_best:
                    best, best_eval = current, current_eval
                    eval_funct.set_best(best, best_eval, scores)        # update best score in eval object

                    # Set baseline for optimizer
                    if self.run_optimizer:
                        self.optimizer.set_baseline_eval(best_eval)

                    if best_eval != Evaluation.MIN_SCORE:
                        self.best_pscore_dict[iterations] = (best_eval, timestamp)
            
            # Option 2: Assign current to best solution in previous iteration
            elif option == 2 and best is not None:
                current = best
                current_eval = best_eval

            if verbose_opt or iterations == 0:
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
                                    eval_funct.get_random_var_bound(),
                                    eval_funct.get_confidence_value(),
                                    eval_funct.RUN_LONGER_TOTAL_GAMES,
                                    eval_funct.get_best()[1],
                                    eval_funct.MIN_SCORE,
                                    None
                                )

        original_eval_config = eval_funct.change_config("NORMAL", new_config_attributes)
        scores, program_eval = eval_funct.evaluate_parallel(program, verbose=True)
        eval_funct.set_config(original_eval_config)

        return scores, program_eval

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
        ):
        epoch = 0
        mutations = 0
        while current_t > final_t:
            best_updated = False
            header = 'Mutated Program'
            timestamp = self.get_timestamp()

            # Mutate current program
            candidate = self.program_mutator.mutate(cp.deepcopy(current), self.closed_list)
            mutations += 1

            # Evaluate the mutated program
            scores, candidate_eval = eval_funct.evaluate(candidate, verbose=True)

            # Run optimizer if flag was specified
            if self.run_optimizer:
                self.ppool.append((candidate, candidate_eval, scores))
                # print('self.ppool_len', len(self.ppool))

                if len(self.ppool) >= self.ppool_max_size:
                    unoptimized_candidate_eval = candidate_eval
                    candidate, candidate_eval, scores, is_optimized = start_optimizer(
                        self.optimizer,
                        self.ppool,
                        self.logger,
                        self.get_timestamp,
                        verbose=verbose_opt
                    )

                    if is_optimized:
                        timestamp = self.get_timestamp()
                        self.unoptimized_pscore_dict[iterations + epoch] = (unoptimized_candidate_eval, timestamp)
                        self.optimized_pscore_dict[iterations + epoch] = (candidate_eval, timestamp)

                    self.ppool = []

            new_best, candidate_eval, scores = self.check_new_best(candidate, candidate_eval, scores, best_eval, eval_funct)
            
            if new_best:
                header = 'New Best Program'
                best_updated = True
                best, best_eval = candidate, candidate_eval

                # Set the best program and its score in eval_funct
                # Since triage is used, the best score in eval_funct must be updated
                eval_funct.set_best(best, best_eval, scores)

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

        return best, best_eval, epoch+1