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

class Plotter:

    def parse_data(self):
        raise Exception('parse_data method not implemented')

    def save_raw(self):
        raise Exception('save_raw method not implemented')

    def plot(self, x, y, title='', xlabel='x', ylabel='y'):
        plt.plot(x, y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(title.replace(' ', '_') + '.jpg')

    def plot_from_data(self, *data, names={}):
        for data_dict in data:
            try:
                x, y = self.parse_data(data_dict)
            except AssertionError:
                return -1
            
            plt.plot(x, y)

        plt.xlabel(names['x'])
        plt.ylabel(names['y'])
        plt.legend(names['legend'], loc='lower right')
        plt.title(names['title'])
        plt.savefig(names['title'].replace(' ', '_') + '.pdf', dpi=300, bbox_inches='tight')