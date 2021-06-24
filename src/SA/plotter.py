"""
SA/plotter.py

Author: Olivier Vadiavaloo

Description:
This module implements 
"""
import src.Utils.plotter as base_plt
import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import join

class Plotter(base_plt.Plotter):

    def parse_data(self, data_dict):
        assert len(data_dict) > 0, 'Empty data dictionary'

        y = []
        for iteration in data_dict.keys():
            score_dict = data_dict[iteration]
            for epoch in score_dict:
                y.append(score_dict[epoch])

        x = list(range(0, len(y)))

        return x, y

    def save_data(self, *data, names=[]):
        DATA_DIR = 'data/'
        count = 0
        for data_dict in data:
            if not os.path.exists(DATA_DIR):
                os.makedirs(DATA_DIR)

            with open(join(DATA_DIR + names[count]), 'w') as data_file:
                data_file.write(f'# {names[count]}')
                x, y = self.parse_data(data_dict)
                for i in range(len(y)):
                    data_file.write(f'{x[i]} {y[i]}\n')

            count += 1