#!/bin/bash

# Make sure environment is set
source env.sh

#equilibrate
cd equilibration
$NAMD_PATH/namd2 +p 4 equilibration.conf > equilibration.log
#*** Make sure to provide the correct path to NAMD in your cluster in above line ***#

python calc_rxn_coor.py > progress_coordinate.dat
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
w_init $BSTATE_ARGS --segs-per-state 4  --work-manager=threads "$@"


# Clean up
rm -f west.log 


# Run dynamics
w_run -r west.cfg --work-manager processes --n-workers 1 "$@" &> west.log

