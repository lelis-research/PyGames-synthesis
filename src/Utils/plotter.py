"""
Utils/plotter.py

Author: Olivier Vadiavaloo

Description:
This module implements a base Plotter class to plot figures
of data generated during synthesis; for example, the evolution
of scores over time.
"""
import matplotlib.pyplot as plt
import numpy as np
import os

class Plotter:

    def parse_data(self):
        raise Exception('parse_data method not implemented')

    def save_data(self):
        raise Exception('save_raw method not implemented')

    def plot(self, x, y, title='', xlabel='x', ylabel='y'):
        plt.plot(x, y)
        plt.title(title)
        plt.xlabel(xlabel)
        step_size = max(1, int(0.1 * len(x)))
        plt.xticks(list(range(x[0], x[-1] + 1, step_size)))
        plt.ylabel(ylabel)
        plt.savefig(title.replace(' ', '_') + '.png')

    def plot_from_data(self, *data, names):
        max_x_len = -1
        for d in data:
            try:
                x, y = self.parse_data(d)
                plt.plot(x, y)
                if len(x) > max_x_len:
                    max_x_len = len(x)
            except AssertionError:
                return -1

        plt.xlabel(names['x'])
        step_size = max(1, int(0.1 * max_x_len))
        plt.xticks(list(range(max_x_len + 1, step_size)))
        plt.ylabel(names['y'])
        plt.legend(names['legend'], loc='lower right')
        plt.title(names['title'])
        plt.savefig(names['title'].replace(' ', '_') + '.png')

    def plot_from_file(self, path, names):
        if not os.path.exists(path):
            raise Exception(f'Path to {path} does not exist')

        with open(path, 'r') as data_file:
            x = []
            y = []
            lines = data_file.readlines()
            for line in lines:
                if line[0] == '#':
                    continue
                
                line_split = line.split()
                x.append(int(line_split[0]))
                y.append(round(float(line_split[1]), 2))

            self.plot(x, y, title=names['title'], xlabel=names['x'], ylabel=names['y'])