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
from src.Evaluation.EvaluationConfig.evaluation_config_cheby import EvaluationConfigCheby
from bayes_opt import BayesianOptimization
from src.SA.plotter import *
from math import ceil
from src.dsl import *
from src.Evaluation.EvaluationConfig.evaluation_config import *
from src.Evaluation.evaluation import *
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

    def calc_batch_size(self):
        # catcher_p = Strategy.new(
        #     IT.new( 
        #         GreaterThan.new( NonPlayerObjectPosition(), Plus.new( PlayerPosition(), Times.new( VarScalar.new('paddle_width'), Constant.new(0.5) ) ) ),
        #             ReturnAction.new( VarFromArray.new('actions', Constant.new(1)) )
        #     ),
        #     Strategy.new( 
        #         IT.new( 
        #             LessThan.new( NonPlayerObjectPosition(), Minus.new( PlayerPosition(), Times.new( VarScalar.new('paddle_width'), Constant.new(0.5) ) ) ), 
        #                 ReturnAction.new( VarFromArray.new('actions', Constant.new(0)) )
        #         ),
        #         ReturnAction.new( VarFromArray.new('actions', Constant.new(2)) )
        #     ),
        # )

        # flappy_bird_p = NestedITEDepth1.new(
        #         LessThan.new( NonPlayerDistToPlayer(), Constant.new(20) ),
        #         Strategy.new(
        #             IT.new(
        #                 LessThan.new( Plus.new( PlayerVelocity(), PlayerPosition() ), Times.new(NonPlayerObjectPosition.new(1), Constant.new(0.8) ) ),
        #                 ReturnAction.new( VarFromArray.new('actions', Constant.new(1)) )
        #             ),
        #             Strategy.new(
        #                 IT.new(
        #                     GreaterThan.new( Plus.new( PlayerVelocity(), PlayerPosition() ), Times.new(NonPlayerObjectPosition.new(0), Constant.new(1.1) ) ),
        #                     ReturnAction.new( VarFromArray.new('actions', Constant.new(0)) )
        #                 ),
        #                 None
        #             )
        #         ),
        #         Strategy.new(
        #             IT.new(
        #                 LessThan.new( Plus.new( PlayerVelocity(), PlayerPosition() ), Times.new(NonPlayerObjectPosition.new(1), Constant.new(0.83) ) ),
        #                 ReturnAction.new( VarFromArray.new('actions', Constant.new(1)) )
        #             ),
        #             Strategy.new(
        #                 IT.new(
        #                     GreaterThan.new( Plus.new( PlayerVelocity(), PlayerPosition() ), Times.new(NonPlayerObjectPosition.new(0), Constant.new(1.1) ) ),
        #                     ReturnAction.new( VarFromArray.new('actions', Constant.new(0)) )
        #                 ),
        #                 None
        #             )
        #         )
        #     )

        pong_p = NestedITEDepth1.new(
            NonPlayerObjectApproaching(),
            Strategy.new(
                IT.new(
                    GreaterThan.new( Minus.new( PlayerPosition(), Times.new( VarScalar.new('paddle_width'), Constant.new(0.85) ) ), NonPlayerObjectPosition() ),
                    ReturnAction.new( VarFromArray.new('actions', Constant.new(0)) )
                ),
                Strategy.new(
                    IT.new(
                        LessThan.new( Plus.new( PlayerPosition(), Times.new( VarScalar.new('paddle_width'), Constant.new(0.85) ) ), NonPlayerObjectPosition() ),
                        ReturnAction.new( VarFromArray.new('actions', Constant.new(1)) )
                    ),
                    ReturnAction.new( VarFromArray.new('actions', Constant.new(2)) )
                )
            ),
            ReturnAction.new( VarFromArray.new('actions', Constant.new(2)) )
        )

        eval_config_attr = form_basic_attr_dict(
            True,
            1,
            0.95,
            50,
            2100,
            Evaluation.MIN_SCORE,
            5
        )

        eval_config_attr[EvaluationConfigCheby.k_eval_name] = 10
        eval_config_attr[EvaluationConfigCheby.by_win_rate_name] = True
        eval_config_factory = EvaluationConfigFactory()
        eval_config = eval_config_factory.get_config('CHEBY', eval_config_attr)
        eval_config.set_best_eval_variance(2.01)

        factory = EvaluationFactory(0, eval_config)
        eval_fun = factory.get_eval_fun('Pong')

        start = time.time()
        scores, avg_score = eval_fun.evaluate(pong_p, verbose=True)
        end = time.time()

        print(f'Running time: {end - start} seconds\n')

        counter = 0
        batch_count = 1
        batch = []
        max_scores = []
        while counter < len(scores):
            batch.append(scores[counter])
            counter += 1
            if counter % 5 == 0:
                print(f'batch {batch_count}: {batch}, stdev {stdev(batch)}, mean: {mean(batch)}, max: {max(batch)}')
                max_scores.append(max(batch))
                batch = []
                batch_count += 1

        print(f'stdev scores {stdev(scores)}')
        print(f'mean scores {round(mean(scores), 2)}')
        print(f'stdev of max scores {stdev(max_scores)}')
        print(f'mean of max scores {round(mean(max_scores), 2)}')
        print(f'returned avg score {avg_score}')


if __name__ == '__main__':

    analytics = Analytics()

    # print('min sample size required: ', analytics.find_min_sample_size(p1, p2, 'Catcher'))

    # min_mean_variance, min_sample = analytics.find_min_games()
    # print(min_mean_variance, min_sample)

    analytics.calc_batch_size()