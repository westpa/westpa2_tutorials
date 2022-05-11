#!/bin/bash
#SBATCH --job-name=nacl
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=25
#SBATCH --output=job_logs/slurm.out
#SBATCH --error=job_logs/slurm.err
#SBATCH --time=72:00:00
#SBATCH --cluster=mpi
#
# run.sh
#
# Run the weighted ensemble simulation. Make sure you ran init.sh first for bash.
#


set -x
cd $SLURM_SUBMIT_DIR
source env.sh || exit 1

env | sort

cd $WEST_SIM_ROOT


# PYTHON, make sure settings are correct in init_and_run.py
python init_and_run.py &> west-${SLURM_JOBID}.log 


# BASH, make sure init.sh is executed first
#w_run --work-manager processes "$@" &> west-${SLURM_JOBID}.log 
