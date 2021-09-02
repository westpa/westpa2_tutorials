This directory contains all the files for performing M-WEM simulation of alanine dipeptide and analyze the results. We will perform M-WEM simulation using the $\Phi$ torsion angle of alanine dipeptide as the milestoning reaction coordinate. But both $\Phi$ and $\Psi$ will be used as weighted ensemble progress coordinate to increase sampling in orthogonal directions. There are total 9 milestones places 20 degrees apart along Phi torsion angle which creats 8 cells. The milestone positions are (-80.0, -60.0, -40.0, -20.0, 0.0, 20.0, 40.0, 60.0, 80.0) degrees. There is one cell between each consecutive pair of milestones.

* ```anchors```: This directory contains the milestone cell anchors (pbd structure files). These files can be obtained from a steered MD simulation as well as from any other pathway finding methods. The location of each anchor is approximately at the middle of the cell. But we are going to perform a restrained equilibration anyway before starting our M-WEM runs

* ```template```: This directory is a generic template for M-WEM simulation for any one cell. It contains all necessary files except for the pdb files which are specific to each cell. Also the ```colvars.in``` files have replacable strings which are used by the ```build.sh``` script to create cell specific files.

* ```build.sh```:  
