import h5py
import numpy
import sys

tau = 20E-12
concentration = 0.0017

scheme = "OVERALL"
n_iterations = 651
xs = numpy.arange(0,n_iterations, dtype='int')

# You can extract the fluxes and normalize manually (involves also running average.py)

# Treat this example as for educational purposes since this is what the rate_evolution
# dataset does automatically.
directh5file = "./ANALYSIS/"+str(scheme)+"/direct.h5"
assignh5file = "./ANALYSIS/"+str(scheme)+"/assign.h5"
populations = h5py.File(assignh5file, 'r')['labeled_populations'][:,0].sum(axis=1)[:n_iterations]  
conditional_fluxes = h5py.File(directh5file, 'r')['conditional_fluxes'][:,0,1][:n_iterations]
conditional_fluxes[numpy.isnan(conditional_fluxes)] = 0
rates = conditional_fluxes/(tau*concentration)
print("extracting conditional fluxes and populations...")
numpy.savetxt('./data_files/conditional_fluxes.dat', numpy.c_[xs, rates[:n_iterations]], fmt='%i %1.4f')       
numpy.savetxt('./data_files/populations.dat', numpy.c_[xs, populations], fmt='%i %1.4f')       

# You can also extract the normalized fluxes directly (no other steps needed; recommended)
original_fluxes = h5py.File(directh5file, 'r')['rate_evolution'][:,0,1]['expected']
original_rates = original_fluxes/(tau*concentration)
print("extracting original rate constants...")
numpy.savetxt('./data_files/original_rates.dat', numpy.c_[xs, original_rates[:n_iterations]], fmt='%i %1.4f')       

if len(sys.argv) > 1:
    if sys.argv[1] == "red":
        red_fluxes = h5py.File(directh5file, 'r')['red_flux_evolution'][:]
        red_rates = red_fluxes/(tau*concentration)
        print("extracting red rate constants...")
        numpy.savetxt('./data_files/red_rates.dat', numpy.c_[xs, red_rates[:n_iterations]], fmt='%i %1.4f')       
