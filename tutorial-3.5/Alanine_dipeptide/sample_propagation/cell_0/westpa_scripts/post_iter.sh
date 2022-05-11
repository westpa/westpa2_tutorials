#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
    set -x
    env | sort
fi

cd $WEST_SIM_ROOT || exit 1

ITER=$(printf "%06d" $WEST_CURRENT_ITER)
tar -cf seg_logs/$ITER.tar seg_logs/$ITER-*.log
rm  -f  seg_logs/$ITER-*.log

WEST_PREV_ITER=$(( WEST_CURRENT_ITER - 1 ))
PREV_ITER=$(printf "%06d" $WEST_PREV_ITER)
find traj_segs/$PREV_ITER -name 'seg.coor' -delete
find traj_segs/$PREV_ITER -name 'seg.xsc' -delete
find traj_segs/$PREV_ITER -name 'seg.vel' -delete

