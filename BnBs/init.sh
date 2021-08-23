#!/bin/bash

# Set up simulation environment
source env.sh

# Clean up from previous/ failed runs
rm -rf *.log traj_segs seg_logs istates west.h5 job_logs west_zmq_* 
mkdir   seg_logs traj_segs istates job_logs

# Set pointer to bstate and tstate
BSTATE_ARGS="--bstates-from bstates/bstates.txt"

# Run w_init
w_init \
  $BSTATE_ARGS \
  --segs-per-state 5 \
#  --work-manager=processes "$@"
