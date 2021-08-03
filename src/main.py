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
from src.Evaluation.evaluation import *
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

def total_games_int(string):
    try:
        value = int(string)
        assert value in range(2, 1001)
        return value
    except:
        raise argparse.ArgumentTypeError('Total games value has to be between 2 and 1000')


def main():

    parser = argparse.ArgumentParser(
            prog='pygame-games-synthesizer',
            usage='%(prog)s [OPTIONS]',
            description='Synthesize strategies',
            epilog='Happy Synthesizing! :-)'
    )

    parser.add_argument('--batch', action='store_true', dest='batch_eval',
                        help='Run batch evaluation')

    parser.add_argument('--config', action='store', dest='config_name', default='sa_default',
                        help='Configuration name for the synthesizer. Used with -mr option.')

    parser.add_argument('-g', '--game', choices=available_games.keys(), dest='game', default='Catcher',
                        help='Game for which a strategy will be synthesized')

    parser.add_argument('--ibr', action='store_true', dest='ibr',
                        help='Run the Iterated Best Response. Will only with 2-player games.')

    parser.add_argument('-l', '--log', action='store', dest='log_file', default='log',
                        help='Name of log file in which results of search will be stored')

    parser.add_argument('-mr', '--multi', type=int, action='store', dest='runs',
                        help='Run synthesizer multi-times. Must specify a config name')

    parser.add_argument('--no-warn', action='store_true', dest='hide_warning',
                        help='Hide warning messages')

    parser.add_argument('-o', '--optimize', action='store_true', dest='optimize',
                        help='Run Bayesian Optimizer on top of synthesizer')

    parser.add_argument('--optimizer-iter', type=int, dest='n_iter', default=25,
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

    parser.add_argument('--save', action='store_true', dest='save_data',
                        help='Save result of search')

    parser.add_argument('--score', type=float, action='store', dest='score_threshold', default=200.00,
                        help='Initial score threshold to be achieved by programs synthesized with BUS')

    parser.add_argument('-s', '-S','--search', action='store', dest='search_algorithm',
                        default='SimulatedAnnealing',
                        help='Search Algorithm (Simulated Annealing or Bottom-Up Search)')

    parser.add_argument('--show-args', action='store_true', dest='show_args',
                        help='Show arguments passed in to synthesizer')

    parser.add_argument('-t', '--time', action='store', dest='time_limit', default=300,
                        help='Running time limit in seconds')

    parser.add_argument('--te', '--triage-eval', type=float, nargs=2, dest='triage_eval',
                        help='Run triage evaluation (can be used with batch evaluation)')

    parser.add_argument('--tg', '--total-games', type=total_games_int, action='store', dest='total_games',
                        default=48, metavar='TOTAL_GAMES', help='Number of games to be played by programs during evaluation')

    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='Logs more information to specified file during synthesis')

    parameters = parser.parse_args()

    algorithm = parameters.search_algorithm
    config_name = parameters.config_name
    time_limit = int(parameters.time_limit)
    log_file = parameters.log_file
    score_threshold = int(parameters.score_threshold)
    is_triage = parameters.triage
    is_optimize_true = parameters.optimize
    is_parallel = parameters.is_parallel
    iterations = parameters.n_iter
    ibr = parameters.ibr
    kappa = parameters.kappa
    sa_option = parameters.sa_option
    verbose = parameters.verbose
    generate_plot = parameters.generate_plot
    save_data = parameters.save_data
    plot_filename = parameters.plot_filename
    total_games = parameters.total_games
    triage_eval = parameters.triage_eval
    batch_eval = parameters.batch_eval
    runs = parameters.runs
    if runs is None:
        runs = 1

    game = parameters.game

    if parameters.hide_warning:
        warnings.filterwarnings('ignore')

    run_optimizer = {
        'run_optimizer': is_optimize_true,
        'iterations': iterations,
        'kappa': kappa, 'triage':is_triage,
        'parallel': is_parallel
        }

    if triage_eval is None:
        triage_eval = (False, None, None)

    elif len(triage_eval) > 0:
        confidence_value = triage_eval[1]
        if confidence_value > 1 or confidence_value < 0:
            raise Exception('Confidence level must be in the interval [0, 1].')

        triage_eval.insert(0, True)

    if batch_eval:
        eval_config_name = 'BATCH'
    else:
        eval_config_name = 'NORMAL'

    multi_runs = []
    if runs > 1:
        multi_runs.append(True)
        multi_runs.append(runs)
        multi_runs.append(config_name)
    else:
        multi_runs.append(False)
        multi_runs.append(1)

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
            game,
            triage_eval,
            eval_config_name,
            sa_option, 
            verbose, 
            generate_plot,
            save_data,
            plot_filename,
            ibr,
            total_games,
            multi_runs.copy()
        )

    if algorithm == 'BUS':
        start_bus(time_limit, log_file, score_threshold, run_optimizer, game)

    if algorithm == 'Probe':
        start_probe(time_limit, log_file, is_parallel, game)


if __name__ == '__main__':
    main()