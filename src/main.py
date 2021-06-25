"""
main.py

Author: Olivier Vadiavaloo

Description:
This module contains the driver code for the synthesizer.
It provides and parses command line arguments that specify options
to run the synthesizer with. For example, the score_threshold, paths
to log files to store the results of the synthesis and an optional
running time limit.
"""
import argparse, warnings
from src.BUS.start_search import start_bus
from src.SA.start_search import start_sa
from src.PROBE.start_search import start_probe
from src.evaluation import *
import numpy as np
import os

os.environ['SDL_VIDEODRIVER'] = 'dummy'

def kappa_float(string):
    try:
        value = float(string)
        assert value in np.arange(0, 10, 0.001).tolist()
        return value
    except:
        raise argparse.ArgumentTypeError('Kappa value has to be between 1 and 10 with 3 decimal places only')


def main():

    parser = argparse.ArgumentParser(
            prog='catcher-synthesizer',
            usage='%(prog)s [OPTIONS]',
            description='Synthesize strategies for Catcher',
            epilog='Happy Synthesizing! :-)'
    )

    parser.add_argument('-g', '--game', choices=Evaluation.available_games, dest='game', default='Catcher',
                        help='Game for which a strategy will be synthesized')

    parser.add_argument('-l', '--log', action='store', dest='log_file', default='log',
                        help='Name of log file in which results of search will be stored')

    parser.add_argument('--no-warn', action='store_true', dest='hide_warning',
                        help='Hide warning messages')

    parser.add_argument('-o', '--optimize', action='store_true', dest='optimize',
                        help='Run Bayesian Optimizer on top of synthesizer')

    parser.add_argument('--optimizer-iter', type=int, dest='n_iter', default=200,
                        help='Number of iterations that the optimization process is run. Must be used with --optimize option')

    parser.add_argument('--optimizer-kappa', type=kappa_float, dest='kappa', default=2.5, metavar='KAPPA',
                        help='Kappa value to use with Bayesian Optimizer. Must be used with --optimize option')

    parser.add_argument('--optimizer-triage', action='store_true', dest='triage',
                        help='Run Bayesian Optimizer with triage. Must be used with --optimize option')

    parser.add_argument('-p', '--parallel', action='store_true', dest='is_parallel',
                        help='Run the optimizer with parallel processing features')

    parser.add_argument('--plot', action='store_true', dest='generate_plot',
                        help='Generate plot during synthesis')
    
    parser.add_argument('--plot-name', action='store', dest='plot_filename', default='plot_file',
                        help='Name of file storing the plotted figure if --plot is specified')
    
    parser.add_argument('--sa-option', type=int, choices=[1, 2], dest='sa_option', default=1,
                        help='Option 1 makes it less likely for SA to be stuck in a local max')

    parser.add_argument('--score', type=float, action='store', dest='score_threshold', default=200.00,
                        help='Initial score threshold to be achieved by programs synthesized with BUS')

    parser.add_argument('-s', '-S','--search', action='store', dest='search_algorithm',
                        default='SimulatedAnnealing',
                        help='Search Algorithm (Simulated Annealing or Bottom-Up Search)')

    parser.add_argument('--show-args', action='store_true', dest='show_args',
                        help='Show arguments passed in to synthesizer')

    parser.add_argument('-t', '--time', action='store', dest='time_limit', default=300,
                        help='Running time limit in seconds')

    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='Logs more information to specified file during synthesis')

    parameters = parser.parse_args()

    algorithm = parameters.search_algorithm
    time_limit = int(parameters.time_limit)
    log_file = parameters.log_file
    score_threshold = int(parameters.score_threshold)
    is_triage = parameters.triage
    is_optimize_true = parameters.optimize
    is_parallel = parameters.is_parallel
    iterations = parameters.n_iter
    kappa = parameters.kappa
    sa_option = parameters.sa_option
    verbose = parameters.verbose
    generate_plot = parameters.generate_plot
    plot_filename = parameters.plot_filename

    game = parameters.game

    if parameters.hide_warning:
        warnings.filterwarnings('ignore')

    run_optimizer = {
        'run_optimizer': is_optimize_true,
        'iterations': iterations,
        'kappa': kappa, 'triage':is_triage,
        'parallel': is_parallel
        }

    if parameters.show_args:
        print('optimizer', run_optimizer)
        print('algorithm', algorithm)
        print('log', log_file)
        print('time_limit', time_limit)
        print('score', score_threshold)
        print('is_parallel', is_parallel)
        input('Press Enter to start search')
    
    if algorithm == 'SimulatedAnnealing':
        start_sa(
            time_limit,
            log_file, 
            run_optimizer, 
            game, sa_option, 
            verbose, 
            generate_plot,
            plot_filename
        )

    if algorithm == 'BUS':
        start_bus(time_limit, log_file, score_threshold, run_optimizer, game)

    if algorithm == 'Probe':
        start_probe(time_limit, log_file, is_parallel, game)


if __name__ == '__main__':
    main()