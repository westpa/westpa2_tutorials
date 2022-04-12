#!/bin/bash



# Make sure environment is set
source env.sh


# Clean up
mv west.log west.log.old


# Run dynamics
w_run -r west.cfg --work-manager processes --n-workers 1 "$@" &> west.log

