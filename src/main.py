"""
main.py

Author: Olivier Vadiavaloo

Description:
This module contains the driver code for the Catcher synthesizer.
It provides and parses command line arguments that specify options
to run the synthesizer with. For example, the score_threshold, paths
to log files to store the results of the synthesis and an optional
running time limit.
"""
import argparse
from src.BUS.start_search import start_bus
from src.SA.start_search import start_sa
from src.evaluation import *
from src.BUS.bus import *
from src.SA.sim_anneal import *

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-search', action='store', dest='search_algorithm',
                        default='SimulatedAnnealing',
                        help='Search Algorithm (Simulated Annealing or Bottom-Up Search)')

    parser.add_argument('-log', action='store', dest='log_file',
                        help='Name of log file in which results of search will be stored')

    parser.add_argument('-score', action='store', dest='score_threshold', default=200,
                        help='Score threshold to be attained by synthesized program by BUS')

    parser.add_argument('-time', action='store', dest='time_limit', default=300,
                        help='Running time limit in seconds')

    parameters = parser.parse_args()

    algorithm = parameters.search_algorithm
    time_limit = int(parameters.time_limit)
    log_file = parameters.log_file
    score_threshold = int(parameters.score_threshold)

    if algorithm == 'SimulatedAnnealing':
        start_sa(time_limit, log_file)

    if algorithm == 'BUS':
        start_bus(time_limit, log_file, score_threshold)


if __name__ == '__main__':
    main()