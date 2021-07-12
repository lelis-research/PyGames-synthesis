"""
analytics.py

Author: Olivier Vadiavaloo

Description:
This module implements the Analytics class which provides handy statistics from
data obtained while running the synthesizer. The .dat files produced from calling
the save_data method of the plotter class can analyzed and the mean, std deviation
and the like can be returned.
"""
import os
from bayes_opt import BayesianOptimization
from src.SA.plotter import *
from math import ceil
from src.dsl import *
from src.evaluation import *
from statistics import *
from src.SA.start_search import *

os.environ['SDL_VIDEODRIVER'] = 'dummy'

class Analytics:

    def analyse_dat_file(self, filepath, name, var_num):
        assert os.path.exists(filepath)

        print('Stats for ', filepath)
        with open(filepath, 'r') as data_file:
            lines = data_file.readlines()

            for line in lines:
                if line[0] == '#':
                    continue
                
                split_line = line.split()
                var = split_line[int(var_num)]
                
                print(f'\tmean of {name}: ', mean(var))
                print(f'\tmedian of {name}:', median(var))
                print(f'\tvariance of {name}:', variance(var))
                print(f'\tstd. deviation of {name}:', stdev(var))

    def launch_search(self, **kwargs):
        arg = kwargs['total_games_played']
        total_games_played = ceil(arg)
        print('total_games_played', total_games_played)

        # init SA variables
        time_limit = 300 * (total_games_played / 5)
        log_file = 'log_find_min_games' + str(self.counter)
        self.counter += 1

        # Turn on optimizer without triage
        run_optimizer = {
            'run_optimizer': True,
            'iterations': 10,
            'kappa': 2.5, 
            'triage': False,
            'parallel': False
        }
        
        game = 'Catcher'
        sa_option = 2
        verbose = False
        generate_plot = False
        save_data = True
        plot_filename = 'find_min_games_graph'
        ibr = False

        print(f'Calling search - {self.counter}')
        # call search
        start_sa(
            time_limit,
            log_file, 
            run_optimizer, 
            game, 
            sa_option, 
            verbose,
            generate_plot,
            save_data,
            plot_filename,
            ibr,
            total_games_played
        )

        # extract variances and find mean
        plotter = Plotter()

        print('Getting variances')
        path = os.path.join('data/' + 'score_variances_find_min_games_data.dat')
        time, variances = plotter.parse_dat_file(path)

        # return negative of mean variance
        return -1 * mean(variances)

    def find_min_games(self):
        self.counter = 0

        print('starting optimizer')
        optimizer = BayesianOptimization(
            f=self.launch_search,
            pbounds={'total_games_played': (5, 50)},
            verbose=0
        )

        optimizer.maximize(
            init_points=2,
            n_iter=5
        )
        
        
        return optimizer.max['target'], optimizer.max['params']


if __name__ == '__main__':

    analytics = Analytics()

    # print('min sample size required: ', analytics.find_min_sample_size(p1, p2, 'Catcher'))

    min_mean_variance, min_sample = analytics.find_min_games()