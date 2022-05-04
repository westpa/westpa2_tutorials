import numpy

n_iterations = 651
window = 100
xs = numpy.arange(1,int(n_iterations/window)+1)

#For block-averaged rates
fi = 0
conditional_fluxes = numpy.genfromtxt("./data_files/conditional_fluxes.dat", usecols=1)
populations = numpy.genfromtxt("./data_files/populations.dat", usecols=1)
block_rates = numpy.zeros(int(n_iterations/window))
for idx, val in enumerate(block_rates):
    flux_average = numpy.mean(conditional_fluxes[fi:fi+window])
    pop_average = numpy.mean(populations[fi:fi+window])
    block_rates[idx] = flux_average/pop_average
    fi += window
numpy.savetxt("./data_files/block_rates.dat", numpy.c_[xs, block_rates], fmt='%i %1.4f')       

#For window averaged rates
xs = numpy.arange(0,n_iterations, dtype='int')
window_rates = numpy.zeros(n_iterations)
for i, value in enumerate(conditional_fluxes):
    starthere = i-window
    if starthere < 0:
        starthere = 0
    uptohere = conditional_fluxes[starthere:i]
    pop_uptohere = populations[starthere:i]
    datapoint = numpy.sum(uptohere)/window
    pop_datapoint = numpy.sum(pop_uptohere)/window
    window_rates[i] = datapoint/pop_datapoint
numpy.savetxt("./data_files/window_rates.dat", numpy.c_[xs, window_rates], fmt='%i %1.4f')       

#For rolling averaged rates
xs = numpy.arange(0,n_iterations, dtype='int')
rolling_rates = numpy.zeros(n_iterations)
for i, value in enumerate(conditional_fluxes):
    starthere = i-window
    if starthere < 0:
        starthere = 0
    starthere = 0
    uptohere = conditional_fluxes[starthere:i]
    pop_uptohere = populations[starthere:i]
    datapoint = numpy.sum(uptohere)/(i+1)
    pop_datapoint = numpy.sum(pop_uptohere)/(i+1)
    rolling_rates[i] = datapoint/pop_datapoint
numpy.savetxt("./data_files/rolling_rates.dat", numpy.c_[xs, rolling_rates], fmt='%i %1.4f')       
