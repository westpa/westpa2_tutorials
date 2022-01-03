import numpy
import matplotlib
import matplotlib.pyplot as plt

ys = numpy.loadtxt("AvgRates_CR.dat", usecols=1)
u_cr = numpy.loadtxt("AvgRates_CR.dat", usecols=2)
l_cr = numpy.loadtxt("AvgRates_CR.dat", usecols=3)

xs = numpy.arange(0,len(ys))

plt.semilogy(xs, ys, color='dodgerblue')
plt.fill_between(xs, l_cr, u_cr, color='dodgerblue', alpha=0.6)
plt.xlim(0,2E3)
plt.ylim(10,2E6)
plt.savefig("bb.png", dpi=300)
