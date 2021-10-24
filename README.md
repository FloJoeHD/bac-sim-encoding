# bac-Sim-QBF-encoding
This repo contains two simple python scripts that generate textfiles including the encoding of the game Sim as a QBF formula.

The output can be further processed with a QBF-Solver to get a solution for the formula if there is one.

The structure is as follows:
* ``encoding_gen.py`` contains the generator for the whole QBF formula
* ``encoding_one_to_three_steps.py`` is a debug/test generator which currently generates 1, 2 or 3 game steps as a QBF formula
* ``sim_encoding.boole`` is the whole QBF formula for the game as textfile in PCNF, generated by ``encoding_gen.py``
* ``testOneToThreeSteps.boole`` is the QBF formula generated by ``encoding_one_to_three_steps.py``
