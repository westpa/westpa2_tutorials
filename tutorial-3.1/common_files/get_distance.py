import mdtraj
import numpy

parent = mdtraj.load('parent.xml', top='bstate.pdb')
traj = mdtraj.load('seg.dcd', top='bstate.pdb')
dist_parent = mdtraj.compute_distances(parent, [[0,1]], periodic=True)
dist_traj = mdtraj.compute_distances(traj, [[0,1]], periodic=True)
dist = numpy.append(dist_parent,dist_traj)
d_arr = numpy.asarray(dist)
d_arr = d_arr*10
numpy.savetxt("dist.dat", d_arr)
