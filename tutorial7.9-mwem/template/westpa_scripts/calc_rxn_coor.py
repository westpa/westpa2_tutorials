import numpy as np


l = np.loadtxt('seg.colvars.traj')

for i in range(len(l)):
    phi = l[i,1]
    psi = l[i,2]
    print("{:.2f}".format(phi), "{:.2f}".format(psi))
