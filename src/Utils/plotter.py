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
from mpl_toolkits import mplot3d

class Plotter:

    def parse_data(self):
        raise Exception('parse_data method not implemented')

    def save_data(self):
        raise Exception('save_raw method not implemented')

    def plot(self, x, y, names, same_fig=False, ax=None, fig=None):
        if not same_fig or (fig is None and ax is None):
            fig, ax = plt.subplots()
        
        ax.plot(x, y)
        ax.set_title(names['title'])
        ax.set_xlabel(names['x'])
        ax.set_ylabel(names['y'])

        if names.get('legend') is not None:
            ax.legend(names['legend'], loc='lower right')

        ax.autoscale()

        if not same_fig:
            fig.savefig(names['filename'] + '.png')
            fig.clf()
            plt.close('all')
            return None, None
        else:
            return fig, ax

    def plot3d(self, x, y, z, names, same_fig=False, ax=None, fig=None):
        if not same_fig or (fig is None and ax is None):
            fig = plt.figure()
            ax = plt.axes(projection='3d')

        ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='None')
        ax.set_title(names['title'])
        ax.set_xlabel(names['x'])
        ax.set_ylabel(names['y'])
        ax.set_zlabel(names['z'])

        if names.get('legend') is not None:
            ax.legend(names['legend'], loc='lower right')
        
        ax.autoscale()

        if not same_fig:
            fig.savefig(names['filename'] + '.png')
            fig.clf()
            plt.close('all')
            return None, None
        else:
            return fig, ax

    def plot_from_data(self, *data, names, three_dim=False):
        fig = None
        ax = None
        for d in data:
            try:
                if three_dim:
                    x, y, z = self.parse_data(d, three_dim)
                    fig, ax = self.plot3d(x, y, z, names, same_fig=True, ax=ax, fig=fig)
                else:
                    x, y = self.parse_data(d, three_dim)
                    fig, ax = self.plot(x, y, names, same_fig=True, ax=ax, fig=fig)
                    ax.legend(names['legend'], loc='lower right')

            except AssertionError:
                return -1

        fig.savefig(names['filename'] + '.png')
        fig.clf()
        plt.close('all')

    def plot_from_file(self, paths, names, same_fig=False, three_dim=False):
        fig = None
        ax = None
        counter = 0
        names['filename'] += '_0'

        for path in paths:
            if not os.path.exists(path):
                raise Exception(f'Path to {path} does not exist')

            if not same_fig and counter > 0:
                new_title = names['filename'].split()   # replace identifier at the end of title
                new_title[-1] = str(counter)
                names['filename'] = ''.join(new_title)

            if three_dim:
                x, y, z = self.parse_dat_file(path, three_dim)
                fig, ax = self.plot3d(x, y, z, names, same_fig, ax, fig)
            else:
                print(path)
                x, y = self.parse_dat_file(path, three_dim)
                fig, ax = self.plot(x, y, names, same_fig, ax, fig)
            
            counter += 1

        if same_fig:
            fig.savefig(names['filename'] + '.png')
            fig.clf()
            plt.close('all')

    def parse_dat_file(self, path, three_dim=False):
        with open(path, 'r') as data_file:
            x = []
            y = []
            z = []
            lines = data_file.readlines()
            for line in lines:
                if line[0] == '#':
                    continue
                
                line_split = line.split()
                x.append(float(line_split[0]))
                y.append(round(float(line_split[1]), 2))
                if three_dim:
                    z.append(round(float(line_split[2]), 2))

            if three_dim:
                return x, y, z
            else:
                return x, y


# if __name__ == '__main__':

#     plotter = Plotter()
#     x = np.linspace(-6, 6, 30)
#     y = np.linspace(-6, 6, 30)

#     X, Y = np.meshgrid(x, y)

#     def f(x, y):
#         return np.sin(np.sqrt(x ** 2 + y ** 2))
    
#     Z = f(X, Y)
    
#     names = {}
#     names['title'] = ''
#     names['x'] = 'x'
#     names['y'] = 'y'
#     names['z'] = 'z'
#     names['filename'] = '3dplot'
#     plotter.plot3d(X, Y, Z, names)