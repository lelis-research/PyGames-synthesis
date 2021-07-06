# PyGames-synthesis
A synthesizer and DSL for generating strategies for playing Catcher game.

## Dependencies

```
pillow
matplotlib
numpy
nose2
Pygame-Learning-Environment
```

## Pygame-Learning-Environment
The PyGames-Synthesis repository provides the implementation of a domain-specific language (DSL) and synthesizers such as Bottom-Up Search, Simulated Annealing and Probe.

It does **not** provide the implementation for the games on which solutions are evaluated at the moment. The games that were used to test the
DSL and the synthesizer were implemented at [Ntasfi's Pygame-Learning-Environment repository](https://github.com/ntasfi/PyGame-Learning-Environment).

### Note:

- I also used an implementation of Pong different from the one in the Pygame-Learning-Environment to test my synthesizer.
  - The reason is that Pong is a 2-player game and it can be beneficial for the search if synthesized strategies play against each other, instead of the same opponent provided by the Pygame-Learning-Environment implementation.
- Any implementation of the games in the Pygame-Learning-Environment should work with the synthesizer and the DSL if the appropriate gamestate and action set are provided to the Evaluation objects in evaluation.py .

## Starting the Synthesizer
Before starting the synthesizer, the files from Pygame-Learning-Environment repository must be placed in the top-level directory.
The directory can be renamed to ```pygame_learning_environment``` to avoid a syntax error when importing the game and required modules.
Then, head to src/evaluation.py and add the following statements at the top of the file to import the PLE class and games for which you want the synthesizer to generate strategies.

```python
from pygame_learning_environment.ple.games.catcher import Catcher
from pygame_learning_environment.ple.ple import PLE
```

If you are using different implementations of the games to generate strategies for, import it here as well.

## Command-line Arguments

Type in the following command in the root directory to see all the optional arguments that be used to configure the synthesizer.

```console
python -m src.main -h
```

The following information should be displayed:

![image](https://user-images.githubusercontent.com/59672031/124525631-2e489c00-ddbd-11eb-951f-fb33b510f8dc.png)

## DSL

The domain-specific language (DSL) that was implemented in [src/DSL.py](https://github.com/olivier-vadiaval/catcher-synthesis/blob/main/src/DSL.py) can be summarized in the
following context-free grammar (CFG):

![image](https://user-images.githubusercontent.com/59672031/124653608-bc269480-de5a-11eb-9630-e78f26e9f15b.png)

where,
* **I** is the initial symbol. 
* The A symbol provides access to an array of 3 actions.
* The D symbol provides arithmetic operations and the domain-specific functions (DSFs) through D1 and D2.
* T provides constants that can be used in the arithmetic operations.
* S1 is the production rule for potentially nested if statements and/or successive if statements.
* S2 adds if-else statements.
* S3 adds for loops to the DSL. The body of the loop can be either S1 or S2.
* B provides comparison operators.
* ε represents an empty string.

## Tests

Unit tests are implemented in tests/ using the unittest module in python. One can also install nose2 and run the following command in the root directory
to execute all the tests:

```console
python -m nose2
```
