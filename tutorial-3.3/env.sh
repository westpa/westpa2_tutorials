#!/bin/bash

### This should point to a directory containing your amber executable, and cpptraj
export AMBERHOME=/opt/installed/amber16/

### Update this to point to the appropriate AMBER executable for your system
# export AMBER_EXEC=$AMBERHOME/bin/sander
export AMBER_EXEC=$AMBERHOME/bin/pmemd.cuda
export CPPTRAJ=$AMBERHOME/bin/cpptraj

### Temporary files/directories will be created under this directory.
### If running on a cluster, this should be node-local, high IO scratch space.
export TEMPDIR_ROOT=/mnt/scratch
