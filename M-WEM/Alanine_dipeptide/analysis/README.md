## Analysis of M-WEM results ##

After the M-WEM simulations are done, it is important to properly analyze the results. We recommend you to refer to the M-WEM manuscript for the theoretical details of the analysis. 

The analysis will be done in two steps:

### Step 1 ###

* Execute the following command ```python analysis_build.py ```. It will produce directories ```cell_0``` through ```cell_7``` and copy the corresponding ```west.h5``` files (WESTPA output files) from the propagation directory into each cell within the ```analysis``` directory. It will also copy the west.cfg files (different from the west.cfg files for propagation), and the analysis.py files from ```westpa_analysis_files``` directory to each cell. The analysis.py file also has strings like "LOW" and "HIGH", which will be replaced by floating ponit numbers corresponding to the left and right milestone.

The analysis.py script produces ```trajectories.pkl```, ```crossings.pkl``` and the ```weights.txt``` files. They contain the information on the trajectory traces (history of the segments in the final iteration), the time and location (which milestone right or left) of the milestone crossings, and the weight each traced trajectory respectively.  

* Perform analysis in all cells by ```./analyze_all_convergence.sh```. This will perform ```python analysis.py``` to produce the .pkl and .txt outputs for the final iteration. But, for the sake of checking convergence of our results, it will also produce similar files for some of the subsequent iterations. To do that, the script will copy the ```analysis.py``` to ```analysis_x.py``` (x = iteration number) and the ```w.niters``` inside analysis.py to the corresponding iteration number. Then it will produce ```trajectories_x.pkl```, ```crossings_x.pkl``` and the ```weights_x.txt``` files for each x.

**Note 1:** This step can take several minutes to a few hours depending on a computing hardware. If you have access to a computing cluster, you may choose to submit this as a job.

**Note 2:** The ```analyze_all_convergence.sh``` script is customizable. For example if you want to run all cells parallelly in a cluster you can create seperate bash script for each cell.

**Note 3:** ```analysis_build.py``` will also produce the following directories for milestoning analysis in Step 2: ```cell_probability```, ```N_i_j_files```, ```R_i_files```, and ```committor```. 
### Step 2 ###

After the analysis of the WESTPA output files are done, we will proceed to analyze our results using the Markovian milestoning framework in two jupyter notebooks: ```kinetics.ipynb``` and ```free-energy-landscape.ipynb```. 

* First run the ```kinetics.ipynb``` notebook to obtain the mean first passage time and the committors. This will also produce the probability distribution file in the milestone space. Details can be found inside the notebook

* Next run the ```free-energy-landscape.ipynb``` to reconstruct the free energy landscape alng Phi and Psi coordinates from the M-WEM data.

**Note:** before executing any notebook set the kernel to the environment in which you installed the MWEM software. If the kernel is not available, activate the jupyter notebook for that environment by executing 

```python -m ipykernel install --user --name=westpa2```

Replace "westpa2" with the environment in which you installed MWEM.
