#!/bin/bash

# Set up environment for westpa
# Actviate a conda environment containing westpa, openmm and mdtraj;
# you may need to create this first (see install instructions)

#conda activate westpa2
export WEST_SIM_ROOT="$PWD"
export SIM_NAME=$(basename $WEST_SIM_ROOT)
