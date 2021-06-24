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
        plt.xticks(list(range(x[0], x[-1] + 1, int(0.1 * len(x)))))
        plt.ylabel(ylabel)
        plt.savefig(title.replace(' ', '_') + '.png')

    def plot_from_data(self, *data, names={}):
        for data_dict in data:
            try:
                x, y = self.parse_data(data_dict)
            except AssertionError:
                return -1
            
            plt.plot(x, y)

        x_len = len(x)
        plt.xlabel(names['x'])
        plt.ylabel(names['y'])
        plt.legend(names['legend'], loc='lower right')
        plt.title(names['title'])
        plt.savefig(names['title'].replace(' ', '_') + '.png')

    def plot_from_file(self, path, names={}):
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