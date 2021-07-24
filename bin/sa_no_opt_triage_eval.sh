#!/bin/bash

# Run synthesizer with the following configuration
# Algorithm: Simulated Annealing
# Game: ${game}
# Time: ${time}
#
# Evaluation: No Multiprocessing (except for long eval's), Use Triage
# Optimizer: None
# 
# plot name: sa_no_optimizer_graph
# .dat files:
#   - all_scores_sa_no_opt_triage_eval_data.dat
#   - best_scores_sa_no_opt_triage_eval_data.dat
#   - score_variances_sa_no_opt_triage_eval_data.da
#
# Log filename: log_[game]_sa_no_opt_triage_eval-[date & time]
# 
# Total games: ${total_games}

game=$1
time=$2
total_games=$3

python -m src.main -t ${time} -l log_${game}_sa_no_opt_triage_eval \
    -g ${game} -s SimulatedAnnealing --tg ${total_games} --te \
    --plot --plot-name sa_no_opt_triage_eval_graph --save \
    --no-warn