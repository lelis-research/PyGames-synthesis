"""
start_search.py 

Author: Olivier Vadiavaloo

Description:
This module implements the driver code of the Simulated Annealing synthesizer.

It declares the operators, dsfs, constants and scalars to be used during
the synthesis process, and calls the synthesizer with the desired arguments.

"""
from src.SA.sim_anneal import *
from src.SA.plotter import *
from src.Evaluation.evaluation import *
from src.Evaluation.EvaluationConfig.evaluation_config import *
from src.Utils.logger import *
from src.Utils.dsl_config import *
from os.path import join

def dump(config_name, data_filename):
    data_filepath = join('data/' + data_filename)
    
    with open(config_name + '_paths', 'a') as paths_file:
        paths_file.write(data_filepath + '\n')

def start_sa(
        time_limit, 
        log_file, 
        run_optimizer, 
        game, 
        triage_eval, 
        eval_config_name,
        sa_option, 
        verbose, 
        plot, 
        save, 
        plot_filename, 
        ibr, 
        total_games, 
        multi_runs
    ):

    if ibr:
        assert available_games[game] == 2, f'Cannot perform IBR on {game}'

    dsl_config = DslConfig('./src/dsl_config.json')
    dsl_config.init_valid_children_types(game)
    grammar = dsl_config.get_grammar(game)

    logger = Logger(
        log_file,
        'Simulated Annealing',
        {**run_optimizer, **{'time': time_limit}}
    )
   
    sa = SimulatedAnnealing(time_limit, logger, run_optimizer)
    triage, random_var_bound, confidence_value = triage_eval
    config_factory = EvaluationConfigFactory()
    config_attributes = form_basic_attr_dict(
        triage,
        random_var_bound,
        confidence_value,
        total_games,
        Evaluation.MIN_SCORE,
        Evaluation.MIN_SCORE,
        5
    )
        
    # if available_games[game] >= 2:
    #     config_attributes[EvaluationConfig.by_win_rate_name] = True

    eval_config = config_factory.get_config(eval_config_name, config_attributes)
    eval_factory = EvaluationFactory(
        0, 
        eval_config
    )

    eval_funct = eval_factory.get_eval_fun(game)
    
    if multi_runs[0]:
        plotter = Plotter()
        total_runs = multi_runs[1]
        for run in range(total_runs):
            n_plot_filename = 'run' + str(run) + '_' + plot_filename
            print(f'Starting run #{run}')
            sa.synthesize(
                grammar, 
                2000, 
                1, 
                eval_funct,
                n_plot_filename, 
                ibr,
                option=sa_option,
                verbose_opt=verbose, 
                generate_plot=plot,
                save_data=save
            )
            print(f'Finishing run #{run}\n')

            data_filenames = plotter.construct_dat_filenames(n_plot_filename)
            config_name = multi_runs[-1]
            dump(config_name, data_filenames['best_scores'])
    
    else:
        sa.synthesize(
            grammar, 
            2000, 
            1, 
            eval_funct,
            plot_filename, 
            ibr,
            option=sa_option,
            verbose_opt=verbose, 
            generate_plot=plot,
            save_data=save
        )