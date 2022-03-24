#!/bin/bash

#SBATCH --job-name=milestoning      ## job name
#SBATCH --account andricio_lab     ## account to charge
#SBATCH -p standard          ## partition/queue name
#SBATCH --nodes=1            ## (-N) number of nodes to use
#SBATCH --cpus-per-task=4    ## number of cores the job needs
#SBATCH -t 72:00:00
#SBATCH --mem=8gb
#SBATCH --error=slurm-%J.err ## error log file

#May need to source the conda.sh file depending on your cluster configuration
#Please use the correct path for your conda.sh. A sample for my cluster is given below:
#source /data/homezvol2/dray1/miniconda3/etc/profile.d/conda.sh


# Make sure environment is set
source env.sh


# Clean up
mv west.log west.log.old 

# Run unrestrained dynamics
w_run -r west.cfg --work-manager processes --n-workers 1 "$@" &> west.log

