#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
    set -x
    env | sort
fi

cd $WEST_SIM_ROOT || exit 1

rm  -f  seg_logs/*.log &
cp west.h5 west_backup.h5
