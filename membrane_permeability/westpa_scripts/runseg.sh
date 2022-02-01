#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

N_GPU=2  # Change as necessary
actual_gid=$((WM_PROCESS_INDEX % N_GPU))
export CUDA_VISIBLE_DEVICES=$actual_gid

# Run the dynamics with OpenMM
python $WEST_SIM_ROOT/common_files/memb_prod.py

#Calculate pcoord with MDTraj
python $WEST_SIM_ROOT/common_files/get_distance.py dist.dat seg.h5
cat dist.dat > $WEST_PCOORD_RETURN

# cp bstate.pdb $WEST_TRAJECTORY_RETURN
cp seg.h5 $WEST_TRAJECTORY_RETURN

cp bstate.pdb $WEST_RESTART_RETURN
cp system.xml $WEST_RESTART_RETURN
cp seg.xml $WEST_RESTART_RETURN/parent.xml

cp seg.nfo $WEST_LOG_RETURN
