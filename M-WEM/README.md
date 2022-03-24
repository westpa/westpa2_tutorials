# Tutorial for Markovian Weighted Ensemble Milestoning (M-WEM)

Author: Dhiman Ray

## Installation link: 
https://github.com/dhimanray/MWEM

## Installation Instruction: 
Go to the MWEM source directory (```mwem```) and enter
```
pip install .
```

Please Install MWEM in the same ebvironment where WESTPA 2.0 is installed.

## Requirements ##

Python3 modules

* numpy
* scipy
* WESTPA 2.0
* matplotlib

MD simulation package

* NAMD 2.14

**Note:** M-WEM is implemented using the colvars module in NAMD. Tutorials can be found in the following links:

* NAMD: http://www.ks.uiuc.edu/Training/Tutorials/namd-index.html

* colvars: https://colvars.github.io/colvars-refman-namd/colvars-refman-namd.html

### Relevant pre-print ###
"Markovian Weighted Ensemble Milestoning (M-WEM): Long-time Kinetics from Short Trajectories" Dhiman Ray, Sharon E. Stone, Ioan Andricioaei, J. Chem. Theory Comput. 2022, 18, 1, 79–95. doi: https://doi.org/10.1021/acs.jctc.1c00803

## Description
This tutotorial covers M-WEM simulation for the gas phase Alanine dipeptide system described in the paper above.  
