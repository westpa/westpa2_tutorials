#!/bin/bash

#SBATCH --job-name=milestoning      ## job name
#SBATCH --account andricio_lab     ## account to charge
#SBATCH -p free          ## partition/queue name
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

#equilibrate
cd equilibration
$NAMD_PATH/namd2 +p 4 equilibration.conf > equilibration.log

python calc_rxn_coor.py > distance.dat
cd ..



# Clean up from previous/ failed runs
rm -rf traj_segs seg_logs istates west.h5 binbounds.txt
mkdir   seg_logs traj_segs istates

#copy files to bstate directory for starting points
cp equilibration/progress_coordinate.dat bstates/progress_coordinate.dat
cp equilibration/milestone_equilibration.restart.coor bstates/seg.coor
cp equilibration/milestone_equilibration.colvars.traj  bstates/seg.colvars.traj
cp equilibration/milestone_equilibration.restart.vel  bstates/seg.vel
cp equilibration/milestone_equilibration.restart.xsc  bstates/seg.xsc
cp common_files/colvars.in bstates/colvars.in

# Set pointer to bstate and tstate
BSTATE_ARGS="--bstate-file $WEST_SIM_ROOT/bstates/bstates.txt"
#TSTATE_ARGS="--tstate-file $WEST_SIM_ROOT/tstate.file"

# Run w_init
w_init $BSTATE_ARGS  --segs-per-state 4  --work-manager=threads "$@"


# Clean up
rm -f west.log 


# Run unrestrained dynamics
w_run -r west.cfg --work-manager processes --n-workers 4 "$@" &> west.log

