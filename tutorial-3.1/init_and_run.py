"""This script demonstrates initializing and running a WESTPA+OpenMM simulation in pure Python"""

import westpa
import westpa.work_managers as work_managers
import os
import shutil

from westpa.cli.core import w_init, w_run
from argparse import Namespace


if __name__ == "__main__":
    
    # Clean up from previous/ failed simulations.
    for i in ['west.h5', 'seg_logs', 'traj_segs', 'istates']:
        try:
            os.remove(i)
        except OSError:
            try:
                shutil.rmtree(i)
            except OSError:
                pass
        
    for i in ['seg_logs', 'traj_segs', 'istates']:
        os.mkdir(i)
    
    # Set some parameters that WESTPA needs to set simulation state.
    args = Namespace(rcfile='west.cfg',
                     verbosity='verbose',
                     work_manager='threads')

    # Update westpa.rc with these
    westpa.rc.process_args(args)

    # Initialize the simulation using the tstate and bstate files
    w_init.initialize(tstates=None, bstates=None,
                      tstate_file='tstate.file', bstate_file='bstates/bstates.txt',
                      segs_per_state=5, shotgun=False)

    # Prepare work manager
    work_managers.environment.process_wm_args(args)

    # Launch the simulation
    w_run.run_simulation()

