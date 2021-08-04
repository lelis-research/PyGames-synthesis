"""
SA/plotter.py

Author: Olivier Vadiavaloo

Description:
This module implements the plotter subclass for plotting the results
of simulated annealing for a given game.
"""
from time import time
from scipy.interpolate import interp1d
import src.Utils.plotter as base_plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import os
from os.path import join

class Plotter(base_plt.Plotter):

    def parse_data(self, data_dict, three_dim):
        # assert len(data_dict) > 0, 'Empty data dictionary'
        if len(data_dict) == 0:
            return np.array([]), np.array([])

        score = []
        time = []
        iteration = []
        for iter, score_time_tuple in data_dict.items():
            score.append(score_time_tuple[0])
            time.append(score_time_tuple[1])
            iteration.append(iter)

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

    def plot_average_curve(self, paths_by_config):
        all_times, all_scores = self.parse_all_paths(paths_by_config)

        min_max_time = self.find_min_max_time(all_times)
        union_time, union_score, union_config_name = self.interpolate_all(min_max_time, all_times, all_scores)

        iter_frame = pd.DataFrame({'score': union_score, 'time': union_time, 'name': union_config_name})

        fig, ax = plt.subplots()
        sns_plot = sb.lineplot(x='time', y='score', hue='name', style='name', ci='sd', markers=False, data=iter_frame)
        ax.set_ylabel('Score')
        ax.set_xlabel('Running Time (mins)')

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles[1:], labels=labels[1:])

        plot_name = 'average_curve'
        sns_plot.get_figure().savefig(plot_name + '.png')
        plt.show()

    def interpolate_all(self, x_upper_bound, times_by_config, scores_by_config):
        union_time = []
        union_score = []
        union_config_name = []
        for config_name, scores_by_config_run in scores_by_config.items():
            for run_index, score in scores_by_config_run.items():
                x_range = np.linspace(0, x_upper_bound, num=50, endpoint=True)

                interpolated_function = interp1d(times_by_config[config_name][run_index], score)
                interpolated_scores = interpolated_function(x_range)

                union_time.extend(x_range)
                union_score.extend(interpolated_scores)
                union_config_name.extend([config_name for _ in range(len(x_range))])

        return union_time, union_score, union_config_name

    def find_min_max_time(self, all_times):
        max_scores = []
        for times_by_config_run in all_times.values():
            for time in times_by_config_run.values():
                max_scores.append(max(time))

        return min(max_scores)

    def parse_all_paths(self, paths_by_config):
        all_scores = {}
        all_times = {}
        for config_name, paths_by_config_run in paths_by_config.items():
            all_scores[config_name] = {}
            all_times[config_name] = {}                
            for run_index, path in paths_by_config_run.items():
                time, score = self.parse_dat_file(path)
            
                all_scores[config_name][run_index] = score
                all_times[config_name][run_index] = time

        print(all_times)
        print(all_scores)
        return all_times, all_scores

    def construct_dat_filenames(self, plot_filename):
        return {
            'all_scores': 'all_scores_' + plot_filename.replace('graph', 'data') + '.dat',
            'best_scores': 'best_scores_' + plot_filename.replace('graph', 'data') + '.dat',
            'unoptimized_scores': 'unoptimized_scores_' + plot_filename.replace('graph', 'data') + '.dat',
            'optimized_scores': 'optimized_scores_' + plot_filename.replace('graph', 'data') + '.dat'
        }

    def construct_paths_by_config(self, dat_filepaths_by_config):
        paths_by_config = {}
        for config in dat_filepaths_by_config:
            paths_by_config[config] = {}

            with open(config, 'r') as dat_filepaths_file:
                dat_filepaths = dat_filepaths_file.readlines()
                for run_index, dat_filepath in enumerate(dat_filepaths):
                    paths_by_config[config][run_index] = dat_filepath

        return paths_by_config


# if __name__ == '__main__':

#     plotter = Plotter()

    # plot_names = {
    #         'x': 'Elapsed Time (mins)',
    #         'y': 'Program Score',
    #         'z': 'Iterations',
    #         'title': 'SA Program Scores vs Total Iterations',
    #         'filename': 'some_graph',
    #         'legend': ['all scores', 'unoptimized scores']
    #     }
    
    # paths = []
    # paths.append(os.path.join('data/' + 'all_scores_no_opt_data.dat'))
    # paths.append(os.path.join('data/' + 'best_scores_unopt_vs_opt_data.dat'))
    # paths.append(os.path.join('data/' + 'unoptimized_scores_no_opt_data.dat'))
    # paths.append(os.path.join('data/' + 'optimized_scores_no_opt_data.dat'))

    # plotter.plot_from_file(paths, plot_names, same_fig=False, three_dim=False)

    # paths_by_config = {
    #     'sa_no_opt_triage_eval_avg_curve': {
    #         0: 'data/best_scores_run0_sa_no_opt_triage_eval_data.dat',
    #         1: 'data/best_scores_run1_sa_no_opt_triage_eval_data.dat',
    #         2: 'data/best_scores_run2_sa_no_opt_triage_eval_data.dat',
    #         3: 'data/best_scores_run3_sa_no_opt_triage_eval_data.dat',
    #         4: 'data/best_scores_run4_sa_no_opt_triage_eval_data.dat'
    #     }
    # }

    # plotter.plot_average_curve(paths_by_config)