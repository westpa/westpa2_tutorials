import mdtraj
import numpy

basis = mdtraj.load('basis.xml', top='bstate.pdb')
dist = mdtraj.compute_distances(basis, [[0,1]], periodic=True)
dist = numpy.asarray(dist)
dist = dist*10
numpy.savetxt("dist.dat", dist)
