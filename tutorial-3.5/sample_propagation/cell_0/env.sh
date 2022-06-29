#!/bin/bash

# Set up environment for westpa
#export WEST_PYTHON=$(which python)
# Actviate a conda environment containing westpa, openmm, mdtraj;
# You may need to create this first (see install instructions)
#source activate westpa2
export WEST_SIM_ROOT="$PWD"
export SIM_NAME=$(basename $WEST_SIM_ROOT)

#Set the path where NAMD is installed in your computer or cluster
export NAMD_PATH="/home/dhiman/NAMD_2.14_Linux-x86_64-multicore" 
