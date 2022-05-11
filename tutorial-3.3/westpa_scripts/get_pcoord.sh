#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
    set -x
    env | sort
fi

cd $WEST_SIM_ROOT

WORK_DIR=`mktemp -d -p $TEMPDIR_ROOT`

echo "west data ref: $WEST_STRUCT_DATA_REF" > $WORK_DIR/wsdata.txt
cp $WEST_STRUCT_DATA_REF $WORK_DIR/parent.rst7
function cleanup() {
    cd $WEST_SIM_ROOT
    rm -rf $WORK_DIR
}

trap cleanup EXIT

# Get progress coordinate
cd $WORK_DIR
mkdir ref_files
cp $WEST_SIM_ROOT/ref_files/reference.pdb ref_files/reference.pdb

$CPPTRAJ $WEST_SIM_ROOT/ref_files/ntl9.prmtop < $WEST_SIM_ROOT/ref_files/ptraj_init.in || exit 1
gawk '{print $2}' rmsd.temp | tail -1 > pcoord.dat || exit 1
cat pcoord.dat > $WEST_PCOORD_RETURN

if [ -n "$SEG_DEBUG" ] ; then
    head -v $WEST_PCOORD_RETURN
fi


