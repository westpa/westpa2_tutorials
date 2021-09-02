This directory contains all the files for performing M-WEM simulation of alanine dipeptide and analyze the results. We will perform M-WEM simulation using the $\Phi$torsion angle of alanine dipeptide as the milestoning reaction coordinate. But both $\Phi$ and $\Psi$ will be used as weighted ensemble progress coordinate to increase sampling in orthogonal directions. 

* ```anchors```: This directory contains the milestone cell anchors (pbd structure files). These files can be obtained from a steered MD simulation as well as from any other pathway finding methods. The location of each anchor is approximately at the middle of the cell. But we are going to perform a restrained equilibration anyway before starting our M-WEM runs

* ```template```:  
