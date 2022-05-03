#!/bin/bash

source env.sh
w_run --work-manager=processes "$@" &> west.log
