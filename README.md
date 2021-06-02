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

```
python -m nose2
```
