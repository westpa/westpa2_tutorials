#!/bin/bash
#
# node.sh

cd $WEST_SIM_ROOT
source env.sh

set -x
w_run "$@"
