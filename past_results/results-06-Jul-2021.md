# Past Experiments

**Date:** 6th July 2021

**Synthesizer:** Simulated Annealing (SA)

**Game:** Catcher

### Method

The synthesizer was run **25** times in total to generate strategies for playing Catcher. That is, there were **5 batches** of **5 experiments**.

Each experiment
* ran for **12 hours (or 43200 seconds)**
* on **16** CPUs
* of **8000Mb** each.

The ```--sa-option``` was set to ```2``` for every experiment. In other words, while the time limit hasn't been reached, the best program found in the previous call to simulated annealing is used as the initial program in the next call, instead of generating a random program again.

This means that once a program has been generated right before the first call to simulated annealing, the best-performing mutated versions of that program are used as initial programs in subsequent calls.

The reduction function used in Simulated Annealing was

<div align='center'>
    <img src='http://www.sciweavers.org/upload/Tex2Img_1625602607/render.png' />
</div>

where ***alpha*** = 0.9, **T<sub>0</sub>** is the initial temperature passed to the algorithm and **T<sub>f</sub>** is the final temperature.

**T<sub>0</sub> = 2000** and **T<sub>f</sub> = 1**. The final and initial temperatures are constant across all experiments.

The acceptance function of the algorithm was

<div align='center'>
    <img src='http://www.sciweavers.org/upload/Tex2Img_1625604021/render.png'>
</div>

where the ***J*** variables are the scores of the current and the mutated programs. ***T*** is the current temperature and ***beta*** is a parameter set to **100** in all experiments.

Hence, the programs' scores are used to determine their performance, or utility, in Catcher. Generally, programs with scores of **at least 1000.0** can be considered strong solutions to the domain.

Since the falling fruit to be caught by the player's paddle spawn at random locations, generated programs need to play the game more than once to obtain a decent estimate of their performance.

In each experiment, the programs play the Catcher game **30 times** and the average score is returned by the evaluation function. 

During optimization, if any is performed, the program to be optimized plays **5 games** in each optimization step. Increasing the number of games played during optimization would significantly slow down the search.

Each experiment in a batch use **5 different configurations** of the synthesizer. However, the configurations remain the same across the batches.

**Experiment 1:** No optimizer

**Experiment 2:** Optimizer without triage

**Experiment 3:** Optimizer with triage

**Experiment 4:** Optimizer without triage, 1000 optimization steps, kappa=5.0

**Experiment 5:** Optimizer with triage, 1000 optimization steps, kappa=5.0

Thus, each experiment is run 5 times and the average scores and variance of the best programs' scores are reported.

### Results

#### Experiment 1

<div align='center'>
    <img src='https://github.com/olivier-vadiaval/PyGames-synthesis/blob/main/graphs/graph_no_optimizer.png' />
</div>

#### Experiment 2

<div align='center'>
    <img src='https://github.com/olivier-vadiaval/PyGames-synthesis/blob/main/graphs/graph_optimizer_no_triage.png' />
</div>

#### Experiment 3

<div align='center'>
    <img src='https://github.com/olivier-vadiaval/PyGames-synthesis/blob/main/graphs/graph_optimizer_triage.png' />
</div>

#### Experiment 4

<div align='center'>
    <img src='https://github.com/olivier-vadiaval/PyGames-synthesis/blob/main/graphs/graph_optimizer_no_triage_1000_iter_5_kappa.png' />
</div>

#### Experiment 5

<div align='center'>
    <img src='https://github.com/olivier-vadiaval/PyGames-synthesis/blob/main/graphs/graph_optimizer_triage_1000_iter_5_kappa.png' />
</div>

___

##### Mean and Standard Deviation

| Experiment | Mean Best Score | Std. Deviation |
|:----------:|:---------------:|:--------------:|
|      1     |     1368.11     |     33.853     |
|      2     |      711.72     | ***995.927***  |
|      3     |     1350.29     |     43.716     |
|      4     |      584.52     | ***806.162***  |
|      5     |     1379.39     |     17.969     |

___

### Results by Batch of Experiments

##### First Batch

| Experiment | Best Score | Optimizer | Triage | Steps | Kappa |
|:----------:|:----------:|:---------:|:------:|:-----:|:-----:|
|      1     | **1401.87**|    No     |   N/A  |  200  |  2.5  |
|      2     |    -2.8    |    Yes    |   No   |  200  |  2.5  |
|      3     |   1378.97  |    Yes    |   Yes  |  200  |  2.5  |
|      4     |    -3.4    |    Yes    |   No   |  1000 |  5.0  |
|      5     |   1369.13  |    Yes    |   Yes  |  1000 |  5.0  |
---
##### Second Batch

| Experiment | Best Score | Optimizer | Triage | Steps | Kappa |
|:----------:|:----------:|:---------:|:------:|:-----:|:-----:|
|      1     |   1364.20  |    No     |   N/A  |  200  |  2.5  |
|      2     | **1520.40**|    Yes    |   No   |  200  |  2.5  |
|      3     |   1377.33  |    Yes    |   Yes  |  200  |  2.5  |
|      4     |    -2.6    |    Yes    |   No   |  1000 |  5.0  |
|      5     |   1372.47  |    Yes    |   Yes  |  1000 |  5.0  |
---
##### Third Batch

| Experiment | Best Score | Optimizer | Triage | Steps | Kappa |
|:----------:|:----------:|:---------:|:------:|:-----:|:-----:|
|      1     |   1312.47  |    No     |   N/A  |  200  |  2.5  |
|      2     |    -3.2    |    Yes    |   No   |  200  |  2.5  |
|      3     |   1293.97  |    Yes    |   Yes  |  200  |  2.5  |
|      4     |   1375.40  |    Yes    |   No   |  1000 |  5.0  |
|      5     | **1409.53**|    Yes    |   Yes  |  1000 |  5.0  |
---
##### Fourth Batch

| Experiment | Best Score | Optimizer | Triage | Steps | Kappa |
|:----------:|:----------:|:---------:|:------:|:-----:|:-----:|
|      1     |   1381.70  |    No     |   N/A  |  200  |  2.5  |
|      2     | **2046.60**|    Yes    |   No   |  200  |  2.5  |
|      3     |   1388.80  |    Yes    |   Yes  |  200  |  2.5  |
|      4     |   1554.40  |    Yes    |   No   |  1000 |  5.0  |
|      5     |   1381.47  |    Yes    |   Yes  |  1000 |  5.0  |
---
##### Fifth Batch

| Experiment | Best Score | Optimizer | Triage | Steps | Kappa |
|:----------:|:----------:|:---------:|:------:|:-----:|:-----:|
|      1     | **1380.30**|    No     |   N/A  |  200  |  2.5  |
|      2     |    -2.4    |    Yes    |   No   |  200  |  2.5  |
|      3     |   1312.40  |    Yes    |   Yes  |  200  |  2.5  |
|      4     |    -1.2    |    Yes    |   No   |  1000 |  5.0  |
|      5     |   1364.37  |    Yes    |   Yes  |  1000 |  5.0  |
---
