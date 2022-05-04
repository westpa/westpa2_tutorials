#!/bin/bash
set -x
cd $WEST_SIM_ROOT/bstates || exit 1
cat progress_coordinate.dat | tail -n 1 > $WEST_PCOORD_RETURN
