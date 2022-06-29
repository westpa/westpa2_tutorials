import numpy as np
import pickle

np.set_printoptions(threshold=np.inf)
import westpa.cli.tools.w_ipa as w_ipa
import mwem.westpa_analysis_functions as we_analysis


w = w_ipa.WIPI()
# At startup, it will load or run the analysis schemes specified in the configuration file (typically west.cfg)
w.main()



tau = 101  #pcoord length from westpa adaptive.py

w.iteration = w.niters
final_trajectories = w.current.seg_id

weights = np.array(w.current.weights)
np.savetxt('weights.txt',weights)
#print(weights)
trajectories = []

for j in range(len(final_trajectories)):
    #trace the trajectory backwards
    traj_trace = w.trace(final_trajectories[j])
    xy = np.array(traj_trace['pcoord'])

    #remove extra frames appearing due to repeating the last frame of previous segment
    traj = we_analysis.remove_extra(traj=xy,tau=tau,num_iterations=w.niters)

    trajectories.append(traj)

#save the trajectories
with open('trajectories.pkl','wb') as f1:
    pickle.dump(trajectories,f1)



#pruning the trajectories
ylow  = LOW
yhigh = HIGH

pruned_trajectories = []
for j in range(len(trajectories)):
    pruned_trajectories.append(we_analysis.pruning(trajectories[j],ylow,yhigh,index=0))

#print(pruned_trajectories[54].shape)
#save the pruned trajectories
with open('pruned_trajectories.pkl','wb') as f1:
    pickle.dump(pruned_trajectories,f1)


crossings = []
for j in range(len(pruned_trajectories)):
    crossings.append(we_analysis.compute_crossings(pruned_trajectories[j],ylow,yhigh))

#save the crossings
with open('crossings.pkl','wb') as f1:
    pickle.dump(crossings,f1)
