Initialize with `init.sh`, and then run with `submit_zmq.sh`


Suggested:
```
sbatch submit_init.sh
sbatch --dependency=afterok:<jobid from first>
```
