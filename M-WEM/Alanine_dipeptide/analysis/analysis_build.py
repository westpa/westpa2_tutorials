import numpy as np
import os
import subprocess

milestones = [-80.0, -60.0, -40.0, -20.0, 0.0, 20.0, 40.0, 60.0, 80.0]

for i in range(len(milestones)-1):

    left = milestones[i]
    right = milestones[i+1]

    dir_name = 'cell_%d'%i

    os.system('mkdir %s'%dir_name)
    os.system('cp ../%s/west.h5 %s/'%(dir_name,dir_name))
    os.system('cp westpa_analysis_files/west.cfg %s/'%dir_name)
    os.system('cp westpa_analysis_files/analysis.py %s/'%dir_name)

    subprocess.call(["sed -i 's/LOW/%0.2f/g' %s/analysis.py"%(left,dir_name)], shell=True)
    subprocess.call(["sed -i 's/HIGH/%0.2f/g' %s/analysis.py"%(right,dir_name)], shell=True)


#create directories for milestoning analysis

os.system('mkdir cell_probability N_i_j_files R_i_files committor')
