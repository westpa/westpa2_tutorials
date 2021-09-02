## Template directory ##

This template directory is virtually identical to the home directory for a regular weighted ensemble simulation using MAB scheme. The only differences are following:

* There is an ```equilibration``` directory, where we perform a short restrained equilibration of the system to bring the milestoning coordinate approximately to the center of the cell. ```equilibration/colvars.in``` is the colvars input file that gradually increase the restrain potential (spring constant) on Phi coordinate over time. ```equilibration/calc_rxn_coor.py``` extract the progress coordinate information from the ```milestoning_equilibration.colvars.traj``` to the```progress_coordinate.dat``` file, which is later read by the WESTPA code.

* There is no structure (pdb) file in equilibration or ```common_files``` directory. These files will be added by the build.py script in a cell specific manner.

* In the ```equilibration/colvars.in``` and ```common_files/colvars.in``` there are terms like "CENTER", "HIGH", and "LOW". These are places where the position of the center and the two milestones are written by the ```build.py``` code. 

* The topology (.psf) and parameter (.prm) files are already provided in the equilibration and ```common_files``` directory, because they are identical for all cells. 

* Two job submissions files (```run.sh``` and ```run.slurm```) are provided. You can use the one which is most suitable for your job submission platform. There is anaother file called ```restart.slurm```. This can be used to restart the simulation. But if you are restarting from a situation where your job crashed in the middle of an iterartion, you should refer to the WESTPA main tutorial about truncating trajectories.

**Note:** In the main WESTPA tutorial you will find two files, ```init.sh``` and ```run.sh```. But we combined them together in one run.sh file (which includes equilibration too), because we found it is easier to submit many files for many milestone cells in this way. 
