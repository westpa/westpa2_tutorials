import numpy as np
import scipy.stats as st

l = np.loadtxt('MFPT_convergence_no_err.dat')

#compute mean and error at 100 iteration by averaging over 
#iteration 60-100

MFPT_list = l[-5:,1]
mean = np.mean(MFPT_list)
conf = st.t.interval(alpha=0.95, df=len(MFPT_list)-1, loc=np.mean(MFPT_list), scale=st.sem(MFPT_list))


print("Mean MFPT (ps) +/-  error (95% confidence interavl)")
print(mean, '+/-', mean-conf[0] )


