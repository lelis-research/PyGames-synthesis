"""
SA/plotter.py

Author: Olivier Vadiavaloo

Description:
This module implements the plotter subclass for plotting the results
of simulated annealing for a given game.
"""
from time import time
import src.Utils.plotter as base_plt
import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import join

class Plotter(base_plt.Plotter):

    def parse_data(self, data_dict, three_dim):
        assert len(data_dict) > 0, 'Empty data dictionary'

        score = []
        time = []
        for iteration in data_dict.keys():
            score_dict = data_dict[iteration]
            for epoch in score_dict:
                score.append(score_dict[epoch][0])
                time.append(score_dict[epoch][1])

        iteration = list(range(0, len(score)))

        X, Y, Z = np.array(iteration), np.array(score), np.array(time)

        if three_dim:
            return X, Y, Z
        else:
            return X, Y

    def save_data(self, *data, names):
        DATA_DIR = 'data/'
        count = 0
        for data_dict in data:
            if not os.path.exists(DATA_DIR):
                os.makedirs(DATA_DIR)

            with open(join(DATA_DIR + names[count]), 'w') as data_file:
                data_file.write(f'# {names[count]}\n')
                x, y, z = self.parse_data(data_dict, True)

                for i in range(len(y)):
                    data_file.write(f'{x[i]} {y[i]} {z[i]}\n')

            count += 1


if __name__ == '__main__':

    plotter = Plotter()

    plot_names = {
            'x': 'Elapsed Time (mins)',
            'y': 'Program Score',
            'z': 'Iterations',
            'title': 'SA Program Scores vs Total Iterations',
            'filename': 'some_graph',
            'legend': ['all scores', 'unoptimized scores']
        }
    
    paths = []
    paths.append(os.path.join('data/' + 'all_scores_no_opt_data.dat'))
    paths.append(os.path.join('data/' + 'best_scores_unopt_vs_opt_data.dat'))
    paths.append(os.path.join('data/' + 'unoptimized_scores_no_opt_data.dat'))
    paths.append(os.path.join('data/' + 'optimized_scores_no_opt_data.dat'))

    plotter.plot_from_file(paths, plot_names, same_fig=False, three_dim=False)