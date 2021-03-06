"""
start_search.py 

Author: Olivier Vadiavaloo

Description:
This module implements the driver code of the Simulated Annealing synthesizer.

It declares the operators, dsfs, constants and scalars to be used during
the synthesis process, and calls the synthesizer with the desired arguments.

"""
from src.SA.sim_anneal import *
from src.SA.program_mutator import *
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


def init_var_child_types(grammar):
        VarArray.valid_children_types = [set(grammar['arrays'])]
        VarFromArray.valid_children_types = [set(grammar['arrays']), set(grammar['array_indexes'])]
        VarScalar.valid_children_types = [set(grammar['scalars'])]
        Constant.valid_children_types = [set(grammar['constants'])]


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
    init_var_child_types(grammar)

    logger = Logger(
        log_file,
        'Simulated Annealing',
        {**run_optimizer, **{'time': time_limit}}
    )

    program_mutator = ProgramMutator(0, 4, 50)
   
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
        
    eval_config = config_factory.get_config(eval_config_name, config_attributes)
    eval_factory = EvaluationFactory(
        0, 
        eval_config
    )

    eval_funct = eval_factory.get_eval_fun(game)

    is_triage_optimizer = run_optimizer['triage']
    n_iter = run_optimizer['iterations']
    kappa = run_optimizer['kappa']
    opt_is_parallel = run_optimizer['parallel']
    is_run_optimizer = run_optimizer['run_optimizer']

    if is_run_optimizer:
        optimizer = Optimizer(
            eval_funct,
            is_triage_optimizer, 
            n_iter, 
            kappa, 
            parallel=opt_is_parallel
        )
    else:
        optimizer = None

    sa = SimulatedAnnealing(time_limit, logger, optimizer, program_mutator)
    
    if multi_runs[0]:
        plotter = Plotter()
        total_runs = multi_runs[1]
        for run in range(total_runs):
            n_plot_filename = 'run' + str(run) + '_' + plot_filename
            print(f'Starting run #{run}')
            sa.synthesize(
                2000, 
                1, 
                eval_funct,
                n_plot_filename, 
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
            2000, 
            1, 
            eval_funct,
            plot_filename, 
            option=sa_option,
            verbose_opt=verbose, 
            generate_plot=plot,
            save_data=save
        )