# Past Experiments

**Date:** 15 Jun 2021

**Synthesizer:** Simulated Annealing

The synthesizer was run 5 times with 5 different configurations, using the following commands.

```console
# Simulated Annealing, No optimizer, Hide Warnings
python -m src.main -S SimulatedAnnealing -t 345600 -l log_sa --no-warn

# Simulated Annealing, Optimizer, No triage, Hide Warnings
python -m src.main -S SimulatedAnnealing -o -t 345600 -l log_sa_opt --no-warn

# Simulated Annealing, Optimizer, Triage, Hide Warnings
python -m src.main -S SimulatedAnnealing -o --optimizer-triage -t 345600 -l log_sa_opt_triage --no-warn

# Simulated Annealing, Optimizer, No Triage, Kappa=5.0, Iterations=1000, Hide Warnings
python -m src.main -S SimulatedAnnealing -o --optimizer-kappa 5.0 --optimizer-iter 1000 -t 345600 -l log_sa_opt_kappa5_iter1000 --no-warn

# Simulated Annealing, Optimizer, No Triage, Kappa=5.0, Iterations=1000, Hide Warnings
python -m src.main -S SimulatedAnnealing -o --optimizer-triage --optimizer-kappa 5.0 --optimizer-iter 1000 -t 345600 -l log_sa_opt_Triage_kappa5_iter1000 --no-warn
```

The running time limit was set to 4 days (345600 seconds), but it can be increased if desired.

As summarized in the comments above, the synthesizer was run with and without an optimizer, with and without a triage option when the optimizer was used, with an increased kappa value and with an increased number of optimization steps (iterations).

These different configurations are specified through command-line arguments as shown above. The usage manual can be found in the [README.md](https://github.com/olivier-vadiaval/catcher-synthesis/blob/main/README.md) file.

The results of each experiment is stored in the user-specified log file in a logs/ directory. The log file is specified using the ```-l``` option. Note that the name is followed by the date and time at which the experiment was launched. For example, if ```-l log_sa_opt``` was used and the experiment was launched at 15:00 on the 15th of June, 2021, then the results will be stored in ```logs/log_sa_opt-15-Jun-2021```.

## Results

| Experiment # |     Synthesizer     |  Optimizer  | Triage | Kappa | Iterations | Running Time | Best Score |
|:------------:|:-------------------:| :---------: |:------:|:-----:|:----------:|:------------:|:----------:|
|      1       | Simulated Annealing |      No     |   No   |  2.5  |    200     |    4 days    |   1569.0   |
|      2       | Simulated Annealing |     Yes     |   No   |  2.5  |    200     |    4 days    | **1662.0** |
|      3       | Simulated Annealing |     Yes     |  Yes   |  2.5  |    200     |    4 days    |   1428.0   |
|      4       | Simulated Annealing |     Yes     |   No   |  5.0  |   1000     |    4 days    |   1110.0   |
|      5       | Simulated Annealing |     Yes     |  Yes   |  5.0  |   1000     |    4 days    |   1428.0   |

```python
# Best Program found by synthesizer in experiment #1
# Simulated Annealing, No optimizer, Hide Warnings
# psize: 17
# score: 1569.0
# Elapsed Time: 50 mins
if PlayerPosition < ((FallingFruitPosition - PlayerPosition) * 59.620000000000005):
        return actions[1]
else:
        return actions[2]
return actions[0] 
```

```python
# Best Program found by synthesizer in experiment #2
# Simulated Annealing, Optimizer, No triage, Hide Warnings
# psize: 35
# score: 1662.0
# Elapsed Time: 6hrs 12 mins
if (PlayerPosition + 2.2058418999301765) > FallingFruitPosition:
        return actions[0]
if (PlayerPosition // ((FallingFruitPosition - (paddle_width - PlayerPosition)) + 7.22)) < FallingFruitPosition:
        return actions[1]
if paddle_width > 18.345999244646677:
        return actions[0]
else:
        return actions[2]

```

```python
# Best Program found by synthesizer in experiment #3
# Simulated Annealing, Optimizer, Triage, Hide Warnings
# psize: 28
# score: 1428.0
# Elapsed Time: 39 mins
if paddle_width < 92.35000000000001:
        return actions[1]
if (FallingFruitPosition + FallingFruitPosition) < (88.0 + ((FallingFruitPosition + 11.36) * (FallingFruitPosition - PlayerPosition))):
        return actions[1]
else:
        return actions[0]
```

```python
# Best Program found by synthesizer in experiment #4
# Simulated Annealing, Optimizer, No Triage, Kappa=5.0, Iterations=1000, Hide Warnings
# psize: 13
# score: 1110.0
# Elapsed Time: 6hrs 48 mins
if PlayerPosition > FallingFruitPosition:
        return actions[0]
else:
        return actions[1]
return actions[1]
```

```python
# Best Program found by synthesizer in experiment #5
# Simulated Annealing, Optimizer, No Triage, Kappa=5.0, Iterations=1000, Hide Warnings
# psize: 13
# score: 1428.0
# Elapsed Time: 9hrs 35 mins
if FallingFruitPosition > (PlayerPosition + 5.21):
        return actions[1]
else:
        return actions[0]
```

## Discussion