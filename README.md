# PyGames-synthesis
A synthesizer and DSL for generating strategies for playing Catcher game.

## Dependencies

```
pillow
matplotlib
numpy
seaborn
pandas
nose2
bayesian-optimization
Pygame-Learning-Environment
```

## Pygame-Learning-Environment
The PyGames-Synthesis repository provides the implementation of a domain-specific language (DSL) and synthesizers such as Bottom-Up Search, Simulated Annealing and Probe.

It does **not** provide the implementation for the games on which solutions are evaluated at the moment. The games that were used to test the
DSL and the synthesizer were implemented at [Ntasfi's Pygame-Learning-Environment repository](https://github.com/ntasfi/PyGame-Learning-Environment).

## Installation

Clone this repository and [Ntasfi's Pygame-Learning-Environment repository](https://github.com/ntasfi/PyGame-Learning-Environment). Rename the __Pygame-Learning-Environment__ directory to ```pygame_games``` and move it to __PyGames-synthesis/__ . You also need to install the module dependencies of both projects. I strongly suggest that you use a virtual environment instead of installing globally.

```console
git clone https://github.com/olivier-vadiaval/PyGames-synthesis.git
git clone https://github.com/ntasfi/PyGame-Learning-Environment.git
pip install -e
```

If you want to use the synthesizer for generating strategies for the Pong domain, please contact me. You can also use a different Pong implementation as long as it implements the methods and attributes used by the game object in EvaluationPong in __src/Evaluation/evaluation_pong.py__ . That is, it should have a step method, be capable of returning a game state as a dictionary, be able to determine if the game is over and have a way to reward strategies in the game.

## Starting the Synthesizer
Run __one__ of the provided bash scripts in __bin/__ to start the synthesizer. Each bash script will run the synthesizer with a specific configuration: with and without triage, with and without optimizer, and whether to run the synthesizer multiple times or once.

To run any given script, one must provide the name of the game (or domain), the time budget, the total number of games to be played during evaluation, the number of times to run the synthesizer, and whether the runs will be executed in separate processes or a single process.

The idea behind being able to run the synthesizer multiple times is to obtain an accurate estimate of the performance of a configuration.

To run a script that does __not__ configure the synthesizer to use triage evaluation, one must specify the __game__, the __time budget__, the __total number of games on which a program is evaluated__, the __number of times__ to run the synthesizer and if there are multiple runs, whether they will be in the same process (__same__) or not (__different__).

To run a script that configures the synthesizer to use triage evaluation, one must specify all of the above and also, a __confidence level__, as well as an __interval size__.

For example, to run the synthesizer __once__ for 300 seconds (5mins) with a 20-game triage evaluation and without any optimizer for the Catcher domain, use the following command __from the root level directory (that is PyGames-synthesis/)__:

```console
sh bin/sa_no_opt_triage_eval.sh Catcher 300 20 0.95 500 1 same
```

0.95 and 500 are the confidence level and the interval size of a program score respectively. If the program score in a given domain can only range between 0 and 1, then the interval size is simply 1. These two values are used during triage to decide whether the evaluation procedure can be stopped as 'we' are confident enough that the current program is worst than the current best.

If one desires to run the synthesizer multiple times (say 10 times) in separate processes, the previous command can be changed to:

```console
sh bin/sa_no_opt_triage_eval.sh Catcher 300 20 0.95 500 10 different 1 first_run
```

__However__, the above command must be run 10 times and on each command, the second to last argument (1 in this case) must be changed to the number of times that the synthesizer has been run. Here, we specify the run index (here it's 1) and an optional suffix (first_run) for building the names of the files holding the results of the experiments. This is to facilitate the parsing of those files to plot graphs and the like. You could build your own script that can call the given scripts multiple times, with your desired suffix for the files containing the experimental results.

To run the synthesizer in one single process, simply change the ```different``` argument to ```same```.

```console
sh bin/sa_no_opt_triage_eval.sh Catcher 300 20 0.95 500 10 same 1 first_run
```

Some imports might have to be fixed in the pygame_games directory. Prefix imports with ```pygame_games.``` in the relevant files for which import errors are raised. Only do this for imports from the pygame_games repo. Do not prefix other imports, such as ```import pygame``` with ```pygame_games.```.

## Command-line Arguments

Type in the following command in a terminal opened from the root directory to see all the command-line arguments that can be used to configure the synthesizer.

```console
python -m src.main -h
```

The following information should be displayed:

```
  -h, --help            show this help message and exit
  --eval-type {CHEBY,NORMAL,BATCH}
                        Run batch evaluation
  --config CONFIG_NAME  Configuration name for the synthesizer. Used with -mr option.
  -g {Catcher,Pong,FlappyBird,Snake}, --game {Catcher,Pong,FlappyBird,Snake}
                        Game for which a strategy will be synthesized
  --ibr                 Run the Iterated Best Response. Will only with 2-player games.
  -l LOG_FILE, --log LOG_FILE
                        Name of log file in which results of search will be stored
  -mr RUNS, --multi RUNS
                        Run synthesizer multi-times. Must specify a config name
  --no-warn             Hide warning messages
  -o, --optimize        Run Bayesian Optimizer on top of synthesizer
  --optimizer-iter N_ITER
                        Number of iterations that the optimization process is run. Must be used with --optimize option
  --optimizer-kappa KAPPA
                        Kappa value to use with Bayesian Optimizer. Must be used with --optimize option
  --optimizer-triage    Run Bayesian Optimizer with triage. Must be used with --optimize option
  -p, --parallel        Run the optimizer with parallel processing features
  --plot                Generate plot during synthesis
  --plot-name PLOT_FILENAME
                        Name of file storing the plotted figure if --plot is specified
  --sa-option {1,2}     Option 1 makes it less likely for SA to be stuck in a local max
  --save                Save result of search
  --score SCORE_THRESHOLD
                        Initial score threshold to be achieved by programs synthesized with BUS
  -s SEARCH_ALGORITHM, -S SEARCH_ALGORITHM, --search SEARCH_ALGORITHM
                        Search Algorithm (Simulated Annealing or Bottom-Up Search)
  --show-args           Show arguments passed in to synthesizer
  -t TIME_LIMIT, --time TIME_LIMIT
                        Running time limit in seconds
  --te TRIAGE_EVAL TRIAGE_EVAL, --triage-eval TRIAGE_EVAL TRIAGE_EVAL
                        Run triage evaluation (can be used with batch evaluation)
  --tg TOTAL_GAMES, --total-games TOTAL_GAMES
                        Number of games to be played by programs during evaluation
  -v                    Logs more information to specified file during synthesis
```

The above command-line arguments can be specified after ```python -m src.main``` to further configure the synthesizer and run it from the command-line without using the provided bash scripts. For instance,

```console
python -m src.main -g Catcher -t 300 -o --optimizer-triage --tg 10
```

## DSL

The domain-specific language (DSL) that was implemented in [src/DSL.py](https://github.com/olivier-vadiaval/catcher-synthesis/blob/main/src/DSL.py) can be summarized in the
following context-free grammar (CFG):

![image](https://user-images.githubusercontent.com/59672031/131167505-a72b2008-4d76-41dd-a6b3-9a69fdc38746.png)

where,
* **I** is the initial symbol. 
* The A symbol provides access to an array of actions.
* The D symbol provides arithmetic operations and the domain-specific functions (DSFs) through D1 and D2.
* T provides constants that can be used in the arithmetic operations.
* S1 is the production rule for potentially nested if statements and/or successive if statements.
* S2 adds if-else statements.
* B provides comparison operators.
* ε represents an empty string.

## Tests

Unit tests are implemented in tests/ using the unittest module in python. One can also install nose2 and run the following command in the root directory
to execute all the tests:

```console
python -m nose2
```
