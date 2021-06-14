# catcher-synthesis
A synthesizer and DSL for generating strategies for playing Catcher game.

## Dependencies

```
numpy
nose2
Pygame-Learning-Environment
```

## Pygame-Learning-Environment
This repository provides the implementation of a domain-specific language (DSL) and a synthesizer using Bottom-Up Search.

It does **not** provide the implementation for the Catcher game at the moment. The Catcher game that was used to test the
DSL and the synthesizer was implemented at [Ntasfi's Pygame-Learning-Environment repository](https://github.com/ntasfi/PyGame-Learning-Environment).

## Starting the Synthesizer
Before starting the synthesizer, the files from Pygame-Learning-Environment repository must be placed in the top-level directory.
The directory can be renamed to ```pygame_learning_environment``` to avoid a syntax error when importing the game and required modules.
Then, head to src/evaluation.py and add the following statements at the top of the file to import the Catcher and the PLE classes.

```python
from pygame_learning_environment.ple.games.catcher import Catcher
from pygame_learning_environment.ple.ple import PLE
```

### Command-line Arguments

Type in the following command in the root directory to see all the optional arguments that be used to configure the synthesizer.

```console
python -m src.main -h
```

The following information should be displayed:

![usage_img](https://user-images.githubusercontent.com/59672031/121953216-83dbdc80-cd1a-11eb-8df2-17d77b53ae34.png)

## DSL

The domain-specific language (DSL) that was implemented in [src/DSL.py](https://github.com/olivier-vadiaval/catcher-synthesis/blob/main/src/DSL.py) can be summarized in the
following context-free grammar (CFG):

```
I → SI | ε

S → if (B) then {A} | if (B) then {A} else {A}

D → D1 | D2

D1 → c1 | c2

D2 → D1 + D1 | D1 - D1 | D1 * D1 | D1 // D1 | D1 * T

T → 0.01 | 0.02 | 0.03 | ... | 0.1 | 0.11 | ... | 1.01 | ... | 100

B → D < D | D > D | D == D

A → actions[0] | actions[1] | actions[2]
```

where,
* **I** is the initial symbol. 
* The A symbol provides access to an array of 3 actions.
* The D symbol provides arithmetic operations and the domain-specific functions (DSFs) through D1 and D2.
* T provides constants that can be used in the arithmetic operations.
* S adds if statements and if-else statements to the language.
* B provides comparison operators.
* ε represents an empty string.

## Tests

Unit tests are implemented in tests/ using the unittest module in python. One can also install nose2 and run the following command in the root directory
to execute all the tests:

```console
python -m nose2
```
