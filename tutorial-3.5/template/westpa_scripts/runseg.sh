#!/bin/bash
#
# runseg.sh
#
# WESTPA runs this script for each trajectory segment. WESTPA supplies
# environment variables that are unique to each segment, such as:
#
#   WEST_CURRENT_SEG_DATA_REF: A path to where the current trajectory segment's
#       data will be stored. This will become "WEST_PARENT_DATA_REF" for any
#       child segments that spawn from this segment
#   WEST_PARENT_DATA_REF: A path to a file or directory containing data for the
#       parent segment.
#   WEST_CURRENT_SEG_INITPOINT_TYPE: Specifies whether this segment is starting
#       anew, or if this segment continues from where another segment left off.
#   WEST_RAND16: A random integer
#
# This script has the following three jobs:
#  1. Create a directory for the current trajectory segment, and set up the
#     directory for running NAMD 
#  2. Run the dynamics
#  3. Calculate the progress coordinates and return data to WESTPA


if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF


# Make symbolic links to the topology file, parameter and colvars files. These are not
# unique to each segment.
ln -sv $WEST_SIM_ROOT/common_files/*.psf .
ln -sv $WEST_SIM_ROOT/common_files/*.pdb .
ln -sv $WEST_SIM_ROOT/common_files/*.prm .
ln -sv $WEST_SIM_ROOT/bstates/colvars.in colvars.in   #make sure the colvars.in is from bstates and not common_files

# Either continue an existing tractory, or start a new trajectory. Here, both
# cases are the same.  If you need to handle the cases separately, you can
# check the value of the environment variable "WEST_CURRENT_SEG_INIT_POINT",
# which is equal to either "SEG_INITPOINT_CONTINUES" or "SEG_INITPOINT_NEWTRAJ"
# for continuations of previous segments and new trajectories, respecitvely.
# For an example, see the nacl_amb tutorial.

# The weighted ensemble algorithm requires that dynamics are stochastic.
# We'll use the "sed" command to replace the string "RAND" with a randomly
# generated seed.
sed "s/RAND/$WEST_RAND16/g" \
  $WEST_SIM_ROOT/common_files/md.conf > md.conf

# This trajectory segment will start off where its parent segment left off.
# The "ln" command makes symbolic links to the parent segment's coor, vel, 
#xsc, and progress_coordinate files. This is preferable to copying the files, 
#since it doesn't require writing all the data again.
if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
  ln -sv $WEST_PARENT_DATA_REF/seg.coor ./parent.coor
  ln -sv $WEST_PARENT_DATA_REF/seg.vel  ./parent.vel
  ln -sv $WEST_PARENT_DATA_REF/seg.xsc  ./parent.xsc
  ln -sv $WEST_PARENT_DATA_REF/progress_coordinate.dat  ./parent.dat

elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  ln -sv $WEST_SIM_ROOT/bstates/seg.coor ./parent.coor
  ln -sv $WEST_SIM_ROOT/bstates/seg.vel  ./parent.vel
  ln -sv $WEST_SIM_ROOT/bstates/seg.xsc  ./parent.xsc
  ln -sv $WEST_SIM_ROOT/bstates/progress_coordinate.dat  ./parent.dat
fi
############################## Run the dynamics ################################
# Propagate the segment using namd2 
$NAMD_PATH/namd2 md.conf > seg.log   

########################## Calculate and return data ###########################


echo "$(pwd)"
python $WEST_SIM_ROOT/westpa_scripts/calc_rxn_coor.py > progress_coordinate.dat
cat progress_coordinate.dat > $WEST_PCOORD_RETURN

# Clean up
mkdir keep
mv seg.coor keep/
mv seg.xsc keep/
mv seg.vel keep/
mv seg.colvars.traj keep/
mv seg.dcd keep/
mv progress_coordinate.dat keep/
rm *
mv keep/* .
rm -r keep
