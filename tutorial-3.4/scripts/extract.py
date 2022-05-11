import h5py
import numpy
import sys

tau = 20E-12
concentration = 0.0017

scheme = "OVERALL"
n_iterations = 651
xs = numpy.arange(0,n_iterations, dtype='int')

directh5file = "./ANALYSIS/"+str(scheme)+"/direct.h5"
assignh5file = "./ANALYSIS/"+str(scheme)+"/assign.h5"
populations = h5py.File(assignh5file, 'r')['labeled_populations'][:,0].sum(axis=1)[:n_iterations]  
conditional_fluxes = h5py.File(directh5file, 'r')['conditional_fluxes'][:,0,1][:n_iterations]
conditional_fluxes[numpy.isnan(conditional_fluxes)] = 0

rates = conditional_fluxes/(tau*concentration)

numpy.savetxt('./data_files/conditional_fluxes.dat', numpy.c_[xs, rates[:n_iterations]], fmt='%i %1.4f')       
numpy.savetxt('./data_files/populations.dat', numpy.c_[xs, populations], fmt='%i %1.4f')       

if len(sys.argv) > 1:
    if sys.argv[1] == "red":
        red_fluxes = h5py.File(directh5file, 'r')['red_flux_evolution'][:]
        red_rates = red_fluxes/(tau*concentration)
        numpy.savetxt('./data_files/red_rates.dat', numpy.c_[xs, red_rates[:n_iterations]], fmt='%i %1.4f')       
