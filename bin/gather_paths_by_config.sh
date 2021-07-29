#!/bin/bash

# This script gathers the paths to the .dat files with the given
# configuration name.
#
# If multiple runs were performed in a SINGLE process, the .dat file
# has "run" prefixing the actual run index. For example:
#
#       best_scores_run5_Catcher_sa_no_opt_data.dat
#
# else the .dat file's name should not contain the prefix and the 
# name of game comes before the run index. For instance:
#
#       best_scores_Catcher_5_sa_no_opt_data.dat
#
# This is to differentiate searches done in different processes/jobs from those
# those done in a single process/job.
#

config=$1
total_runs=$2
game=$3
was_single_process=$4
paths_file=${config}_paths
touch $paths_file

rm ${paths_file}

for ((i=0; i < $total_runs; i++)) {
    if [ -z "$was_single_process" ]
        then
            echo "best_scores_${game}_${i}_${config}_data.dat" >> ${paths_file}
        else
            echo "best_scores_run${i}_${game}__${config}_data.dat" >> ${paths_file}
    fi
}