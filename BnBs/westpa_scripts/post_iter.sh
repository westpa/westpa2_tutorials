#!/bin/bash

set -x

cd $WEST_SIM_ROOT || exit 1

ITER=$(printf "%06d" $WEST_CURRENT_ITER)
TAR=$(($WEST_CURRENT_ITER-1))
TAR_DIR=$(printf "%06d" $TAR)
echo $ITER
echo $TAR
echo $TAR_DIR
tar -cf seg_logs/$ITER.tar seg_logs/$ITER-*.log
rm  -f  seg_logs/$ITER-*.log
if [ -d traj_segs/$TAR_DIR ]; then
  tar -cf traj_segs/$TAR_DIR.tar traj_segs/$TAR_DIR
  rm -rf traj_segs/$TAR_DIR
fi

BACKUPINTERVAL=100
CHECK=$(python -c "print($WEST_CURRENT_ITER%$BACKUPINTERVAL)")
if [ "${CHECK}" == "0" ]; then
  cp ${WEST_SIM_ROOT}/west.h5 ${WEST_SIM_ROOT}/west.h5.backup1
  mv ${WEST_SIM_ROOT}/west.h5.backup1 ${WEST_SIM_ROOT}/west.h5.backup2
fi

