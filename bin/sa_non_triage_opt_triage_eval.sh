#!/bin/bash

# Run synthesizer with the following configuration
# Algorithm: Simulated Annealing
# Game: ${game}
# Time: ${time}
#
# Evaluation: No Multiprocessing (except for long eval's), Use Triage 
# Optimizer: Yes & No Triage, 10 iterations, 9
# 
# plot name: sa_no_optimizer_graph
# .dat files:
#   - all_scores_sa_non_triage_opt_triage_eval_data.dat
#   - best_scores_sa_non_triage_opt_triage_eval_data.dat
#   - score_variances_sa_non_triage_opt_triage_eval_data.da
#
# Log filename: log_[game]_sa_non_triage_opt_triage_eval-[date & time]
# 
# Total games: ${total_games}
config="sa_non_triage_opt_triage_eval"

game=$1
time=$2
total_games=$3
confidence=$4
var_bound=$5
multi_run=$6
same_process=$7
run_index=$8

if [ "$multi_run" = "1" ]
    then
        mr=""
        run_index=""
    else
        if [ "$same_process" = "same" ]
            then
                mr="-mr ${multi_run}"   # same process will run SA multiple times
                run_index=""            # user doesn't need to specify a run index
            else
                mr=""
                if [ -z "$run_index" ]
                    then
                        run_index=1     # user needs a run index, default value is 1
                fi

                echo "run index: $run_index"
        fi
fi

log_name=log_${run_index}_${game}_${config}
plot_name=${game}_${run_index}_${config}_graph

echo "log file: ${log_name}"
echo "plot name: ${plot_name}"

python -u -m src.main -t ${time} -l ${log_name} \
    -o \
    -g ${game} -s SimulatedAnnealing --tg ${total_games} --te ${var_bound} ${confidence} \
    --plot --plot-name ${plot_name} --save --config ${config} \
    ${mr} \
    --no-warn >> /dev/null 2>&1 &