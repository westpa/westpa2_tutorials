#!/bin/bash
set -x
cd $WEST_SIM_ROOT/bstates || exit 1
cat pcoord.init > $WEST_PCOORD_RETURN

cp $WEST_SIM_ROOT/common_files/bstate.pdb $WEST_TRAJECTORY_RETURN
cp $WEST_STRUCT_DATA_REF $WEST_TRAJECTORY_RETURN

cp $WEST_SIM_ROOT/common_files/bstate.pdb $WEST_RESTART_RETURN
cp $WEST_SIM_ROOT/common_files/system.xml $WEST_RESTART_RETURN
cp $WEST_STRUCT_DATA_REF $WEST_RESTART_RETURN/parent.xml
