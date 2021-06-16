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

## Method

The running time limit was set to **4 days** (345600 seconds), but it can be increased if desired. The synthesizer in each experiment used **6 CPUs** with a minimum of **8000Mb** each.

The DSL is implemented in src/dsl.py, which also contains the accepted types of child nodes of each non-terminal node class.

As summarized in the comments above, the synthesizer was run with and without an optimizer, with and without a triage option when the optimizer was used, with an increased kappa value and with an increased number of optimization steps (iterations).

These different configurations are specified through command-line arguments as shown above. The usage manual can be found in the [README.md](https://github.com/olivier-vadiaval/catcher-synthesis/blob/main/README.md) file.

The results of each experiment is stored in the user-specified log file in a logs/ directory. The log file is specified using the ```-l``` option. Note that the name is followed by the date and time at which the experiment was launched. For example, if ```-l log_sa_opt``` was used and the experiment was launched at 15:00 on the 15th of June, 2021, then the results will be stored in ```logs/log_sa_opt-15-Jun-2021```.

## Results

|  Experiment  |     Synthesizer     |  Optimizer  | Triage | Kappa | Iterations | Running Time | Best Score |
|:------------:|:-------------------:| :---------: |:------:|:-----:|:----------:|:------------:|:----------:|
|      1       | Simulated Annealing |      No     |  N/A   |  N/A  |    N/A     |    4 days    |   1569.0   |
|      2       | Simulated Annealing |     Yes     |   No   |  2.5  |    200     |    4 days    | **1662.0** |
|      3       | Simulated Annealing |     Yes     |  Yes   |  2.5  |    200     |    4 days    |   1428.0   |
|      4       | Simulated Annealing |     Yes     |   No   |  5.0  |   1000     |    4 days    |   1110.0   |
|      5       | Simulated Annealing |     Yes     |  Yes   |  5.0  |   1000     |    4 days    |   1428.0   |

### Experiment 1
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

### Experiment 2
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

### Experiment 3
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

### Experiment 4
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

### Experiment 5
```python
# Best Program found by synthesizer in experiment #5
# Simulated Annealing, Optimizer, Triage, Kappa=5.0, Iterations=1000, Hide Warnings
# psize: 13
# score: 1428.0
# Elapsed Time: 9hrs 35 mins
if FallingFruitPosition > (PlayerPosition + 5.21):
        return actions[1]
else:
        return actions[0]
```

### My Own Hand-Written Solution
```python
# psize: 20
# score: 1637.0
if FallingFruitPosition > (PlayerPosition + (paddle_width // 2)):
            return actions[1]
if FallingFruitPosition < (PlayerPosition - (paddle_width // 2)):
    return actions[0]
```

## Discussion

- In the first experiment, no optimizer was used on top of the synthesizer and the best synthesized program, with a score of 1569.0 and size of 17, was obtained after 50 mins only. I consider any solution obtaining a score **higher than 1000.0** to be strong.
    
    - Hence, this shows that simulated annealing performs well enough without any optimizer and can find a very good solution in less than an hour.
    
    - However, the program does not do as well when assessed in terms of interpretability. It contains a constant value that does not make much sense to a human and the last return statement is unreachable.

- In the second experiment, the bayesian optimizer was used without triage, with a kappa value of **2.5** and **200** optimization steps. The best solution, with a size of 35 and a score of 1662.0, was found after 6hrs 12 mins.
    
    - This program is slightly stronger than my own hand-written solution which has a score of 1637.0 It was found in a decent amount of time and did not need any optimization.
    
    - Nevertheless, the solution does not do very well in terms of interpretability too, as it is larger in size and contains two constants that wouldn't make much sense to a human. 
    
    - However, it seems that if the first two if-statements don't evaluate to True, the following if-else statement checks if the paddle is greater than a certain size - **18** in this case - the solution moves the paddle to the left, otherwise it returns the NOOP actions (that is, the paddle is not moved).

    - The optimization also yielded interesting results, despite not having found better parameters for the best solution. The optimizer enabled the synthesizer to improve bad and moderately good solutions into strong ones.
        
        - For example, the following program had a score of **-3** and after the optimization, it obtained a score **1110.0**.


        ```python
        if (paddle_width // 100.001) > ((paddle_width + 83.86602909783636) // (FallingFruitPosition - PlayerPosition)):
            return actions[0]
        else:
            return actions[1]
        return actions[2]
        ```


        - The optimizer can then lead to finding more solutions with large scores, by improving on poorly performing solutions generated by simulated annealing.

- In the third experiment, the bayesian optimizer was used with **triage**, a kappa value of **2.5** and **200** optimization steps. The best solution, with a size of 28 and a score of 1428.0, was obtained after 39 mins only.

    - The program achieves a strong score again, but is not able to beat the previous two solutions.
    
    - The optimization does not seem to perform as well as in experiment 2 here and the reason is likely because the number of optimization steps is too small, which makes it more likely for the optimize method to return after the first batch of optimization steps. This is because the local space of parameters hasn't been explored enough to improve the score of the solution.

- In the fourth experiment, the bayesian optimizer was used without triage, an increased kappa value of **5** and an increased number of optimization steps of **1000**. The best solution obtained a score 1110.0, had a size of 13 and was found after 6hrs 48 mins.
    
    - The program has the lowest score across experiments and the reason might be because the search is slowed down by the optimizer which has to perform 1000 optimization steps.
    
    - Besides, the optimizer cannot explore the neighbourhood of the parameter values well enough to find better ones since the kappa value is large.
    
    - That probably explains why no optimized program could achieve a positive score.

- In the last experiment, the bayesian optimizer was used with triage, a kappa value of **5** and **1000** optimization steps. The best program achieved a score of 1428.0, just like in the third experiment. It has a size of 13 and was found after 9hrs 35 mins.
    
    - Therefore, the program performs strongly and it is more interpretable than the previous solutions.
    
    - It is the smallest in size with the program from experiment 4. It consists of a simple if-else statement that compares the position of the paddle and the falling fruit. It moves the paddle to the right if the fruit is on the right and moves it to the left if the fruit is on the left.
    
    - It also contains a constant value, which was not optimized and it is likely because the optimization stopped right after the first two or first three batches of optimization steps. The higher kappa value might also be preventing the optimizer from exploring the parameter's local space well, hence why not many programs were optimized successfully.

- Overall, one can note that running simulated annealing without any optimization can yield a strong solution and that using an optimizer can lead to even better results. According to the results, the most effective configuration for the optimizer is to not use any triage, a reasonably small kappa value, such as 2.5, and a large number of optimization steps, possibly greater than 1000.