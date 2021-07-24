#!/bin/bash

# Run synthesizer with the following configuration
# Algorithm: Simulated Annealing
# Game: ${game}
# Time: ${time}
#
# Evaluation: No Multiprocessing (except for long eval's), No Triage 
# Optimizer: None
# 
# plot name: sa_no_optimizer_graph
# .dat files:
#   - all_scores_sa_no_optimizer_data.dat
#   - best_scores_sa_no_optimizer_data.dat
#   - score_variances_sa_no_optimizer_data.da
#
# Log filename: log_[game]_sa_no_optimizer-[date & time]
# 
# Total games: ${total_games}

game=$1
time=$2
total_games=$3

python -m src.main -t ${time} -l log_${game}_sa_no_optimizer \
    -g ${game} -s SimulatedAnnealing --tg ${total_games} \
    --plot --plot-name sa_no_optimizer_graph --save \
    --no-warn