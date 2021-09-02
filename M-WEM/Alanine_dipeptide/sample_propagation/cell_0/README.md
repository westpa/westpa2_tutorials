## Sample Cell ##

This a sample of how the directory of a cell (the cell 0 to be specific), created by the ```build.py``` would look like. The ```Aladipep.pdb``` file in ```equilibration``` and ```common_files``` directory are a copy of the ```cell_0.pdb``` from the ```anchors``` directory. The simulation job can be submitted using ```run.sh``` or ```run.slurm```.

**Note:** Depending on the computing system you are using this simulation can take several hours. For test runs, it is recommended to decrease the maximum number of interations in the ```west.cfg``` file (```max_total_iterations: 100```) to a lower value. 
