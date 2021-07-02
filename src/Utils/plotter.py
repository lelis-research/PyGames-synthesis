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

    def plot(self, x, y, names):
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title(names['title'])
        ax.set_xlabel(names['x'])
        ax.set_ylabel(names['y'])

        ax.autoscale()

        fig.savefig(names['filename'] + '.png')
        fig.clf()
        plt.close('all')

    def plot_from_data(self, *data, names):
        max_x_len = -1
        fig, ax = plt.subplots()
        for d in data:
            try:
                x, y = self.parse_data(d)
                ax.plot(x, y)
                if len(x) > max_x_len:
                    max_x_len = len(x)
            except AssertionError:
                return -1

        ax.set_xlabel(names['x'])
        ax.set_ylabel(names['y'])
        ax.legend(names['legend'], loc='lower right')
        ax.set_title(names['title'])

        ax.autoscale()

        fig.savefig(names['filename'] + '.png')
        plt.close(fig)

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

            self.plot(x, y, names)