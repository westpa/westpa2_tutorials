import numpy
import matplotlib
import matplotlib.pyplot as plt
import sys

#Define our x values
xs = numpy.arange(0,13.02,0.02)

#Load in our rate constants
pre_ys_block  = numpy.loadtxt("./data_files/block_rates.dat", usecols=1)
ys_window     = numpy.loadtxt("./data_files/window_rates.dat", usecols=1)
ys_rolling    = numpy.loadtxt("./data_files/rolling_rates.dat", usecols=1)

#Make our block averaged rate constants appear continuous
ys_block = numpy.zeros((ys_window.shape[0]))
a = 0
b = 2
for idx, val in enumerate(ys_block):
    if idx >= 600:
        ys_block[idx] = pre_ys_block[-1]
        continue
    if xs[idx] < b:
        ys_block[idx] = pre_ys_block[a]
    elif xs[idx] == b:
        a += 1
        b += 2
        ys_block[idx] = pre_ys_block[a]
    
#Experimental value line
experiment = numpy.zeros((ys_window.shape[0]))
experiment_u = numpy.zeros((ys_window.shape[0]))
experiment_l = numpy.zeros((ys_window.shape[0]))
for idx, val in enumerate(experiment):
    experiment[idx] = 2.86E8
    experiment_u[idx] = 3.53E8
    experiment_l[idx] = 2.19E8

#Create figure/axis and plot the three curves
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)

if len(sys.argv) > 1:
    if sys.argv[1] == "red":
        ys_red    = numpy.loadtxt("./data_files/red_rates.dat", usecols=1)
        ax.semilogy(xs, ys_rolling, linewidth=2, label="standard")
        ax.semilogy(xs, ys_red, linewidth=2, label="red")
        ax.semilogy(xs, experiment, '--', linewidth=2, color="grey", label="experiment")
        ax.fill_between(xs, experiment_u, experiment_l, color="grey", alpha=0.4)
else:
    ax.semilogy(xs, ys_block, linewidth=2, label="block")
    ax.semilogy(xs, ys_window, linewidth=2, label="window")
    ax.semilogy(xs, ys_rolling, linewidth=2, label="rolling")
    ax.semilogy(xs, experiment, '--', linewidth=2, color="grey", label="experiment")
    ax.fill_between(xs, experiment_u, experiment_l, color="grey", alpha=0.4)

ax.tick_params(axis='both', labelsize=20)
plt.xlabel("molecular time (s)", fontsize=28)
plt.ylabel("rate constant estimate (M$^{-1}$ s$^{-1}$)", fontsize=28)
plt.xlim(0, xs[-1])
plt.tight_layout()
plt.legend(fontsize=20)

#Save plot

if len(sys.argv) > 1:
    if sys.argv[1] == "red":
        plt.savefig("./images/rate_constants_red.png")
else:
    plt.savefig("./images/rate_constants.png")
