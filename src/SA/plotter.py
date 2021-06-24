"""
SA/plotter.py

Author: Olivier Vadiavaloo

Description:
This module implements 
"""
import src.Utils.plotter as base_plt
import matplotlib.pyplot as plt
import numpy as np

class Plotter(base_plt.Plotter):

    def parse_data(self, data_dict):
        assert len(data_dict) > 0, 'Empty data dictionary'

        y = []
        for iteration in data_dict.keys():
            score_dict = data_dict[iteration]
            for epoch in score_dict:
                y.append(score_dict[epoch])

        x = np.linspace(0, len(y), len(y), endpoint=True)

        return x, y