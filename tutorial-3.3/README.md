# Tutorial 3.3: Analysis and Restarting with haMSMs: NTL9 Protein Folding
This tutorial demontrates the use of an haMSM restarting workflow in WE simulations of the ms-timescale folding process of the NTL9 protein.

## Tutorial files

All files necessary for completing the tutorial can be downloaded using the included script.
Additional software needs to be installed to complete the tutorial.


## Instructions
Initialize with `init.sh`, and then run with `submit_zmq.sh`


Suggested:
```
sbatch submit_init.sh
sbatch --dependency=afterok:<jobid from first>
```

## Authors

* **John Russo** - *Primary work* - [jdrusso](https://github.com/jdrusso)
