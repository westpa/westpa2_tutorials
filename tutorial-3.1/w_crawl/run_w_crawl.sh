#!/bin/bash

# Do this if you are using one node:
w_crawl \
  wcrawl_functions.calculate \
  -c wcrawl_functions.crawler \
  -W west.h5 \
  --last-iter 2 \
  --serial \
  &> w_crawl.log 

# Do this (uncomment) if you are using multiple nodes:
#SERVER_INFO=${ANALYSIS_DIR}_west_zmq_info-$WEST_JOBID.json
#echo $WEST_JOBID
#
## start dedicated server
#$WEST_ROOT/bin/w_crawl \
#  wcrawl_functions.calculate \
#  -c wcrawl_functions.crawler \
#  --debug \
#  --last-iter 200 \
#  --work-manager=zmq \
#  --n-workers=0 \
#  --zmq-mode=server \
#  --zmq-info=$SERVER_INFO \
#  &> ${ANALYSIS_DIR}/w_crawl-$WEST_JOBID.log & 
#
## Wait on host info file up to 5 minutes
#for ((n=0; n<30; n++)); do
#  date
#  if [ -e $SERVER_INFO ] ; then
#    echo "== server info file $SERVER_INFO =="
#    cat $SERVER_INFO
#    break
#  fi
#  sleep 10
#done
#
## Exit if host info file doesn't appear in time
#if ! [ -e $SERVER_INFO ] ; then
#  echo 'server failed to start'
#  kill %1
#  exit 1
#fi
#
#
## Start clients
#srun \
#  --ntasks=${SLURM_NNODES} \
#  --ntasks-per-node=1 \
#  --mpi=pmi2 \
#  ${ANALYSIS_DIR}/node.sh \
#    --verbose \
#    --n-workers=16 \
#    --work-manager=zmq \
#    --zmq-mode=client \
#    --zmq-info=$SERVER_INFO &
#wait
