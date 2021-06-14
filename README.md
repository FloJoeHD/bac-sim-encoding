# bac-sim-QBF-encoding
A simple python script that generates a textfile which includes the encoding of the Sim game as a QBF formula.

This can be then further processed with a QBF-Solver to get a solution for the formula if there is one.

The structure is as follows:
* encoding_gen.py contains the generator for the whole QBF formula
* encoding_one_step.py is a debug/test generator which currently generates 1 or 2 game steps as a QBF formula
* output_web was the output of limboole web interface of a formula which still contained errors (so not relevant anymore)
* sim_encoding.boole is the whole QBF formula for the game as textfile in PCNF, generated by encoding_gen.py
* testOneStep.boole is the QBF formula generated by encoding_one_step.py
