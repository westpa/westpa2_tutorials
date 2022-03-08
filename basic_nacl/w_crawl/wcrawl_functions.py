from __future__ import print_function, division; __metaclass__ = type
import os
import sys
import io
import tarfile
import numpy
import mdtraj
import h5py
from westpa.core import h5io
from westpa.core.segment import Segment
from westpa.cli.tools.w_crawl import WESTPACrawler
from itertools import combinations 


class IterationProcessor(object):
    '''
    This class performs analysis on each iteration.  It should contain a method
    ``process_iteration``, which may be called as 
    ``process_iteration(self, n_iter, iter_group)``, where ``n_iter`` refers to
    the weighted ensemble iteration index, and ``iter_group`` is the HDF5 group 
    for the given iteration. The method should return an array or other values, 
    which the ``process_iter_result`` method of the ``Crawler`` class recieves 
    as the argument ``result``. 
    '''
    # Store the location of the PDB file to be used as the topology 
    topfile = './bstate.pdb'
    # Define the pattern used for finding each segment's traj file
    h5iter_pattern = 'iterations/iter_{n_iter:08d}'
    h5traj_pattern = 'traj_segs/iter_{n_iter:06d}.h5'
    parent_pattern = 'traj_segs/parent_{n_iter:06d}{n_seg:06d}'
    start_pattern = 'bstates/{auxref}/basis.xml'

    def __init__(self):
        '''
        Initialize the IterationProcessor class
        '''
    def process_iteration(self, n_iter, iter_group):
        '''
        The main analysis function that w_crawl calls for each iteration.
        This should be changed based on your analysis. This method could
        contain all the code for your analysis, or it could call an outside
        function. 

        ----------
        Parameters
        ----------
        n_iter: (int) The index of the weighted ensemble iteration for which
          analysis should be performed.
        iter_group: (H5py group) The hdf5 group corresponding to iteration
          n_iter, from the the main WESTPA data file (typically west.h5)

        -------
        Returns
        -------
        result: (numpy.ndarray) In general this could be an object, which is
          later processed by Crawler.process_iter_result. Here, it is an array
          of the center of mass of the protein. The array has shape 
          (n_segments, n_timepoints, 3), where dimension 0 indexes the segment, 
          dimension 1 indexes the frame number, and dimension 2 indexes the 
          x/y/z coordinate of the center of mass.
        '''
        # Find the number of segments in the iteration at hand
        print("starting",n_iter)
        num_segs = iter_group['seg_index'].shape[0]
        parent_iter = n_iter-1

        frames_per_iter = 50
        num_atoms = 4010
        data_dims = 3

#        h5file = h5py.File("west.h5", "r")
#        parent_seg_arr = h5file[self.h5iter_pattern.format(n_iter=n_iter)]["seg_index"]["parent_id"]
#        bstate_id_arr = h5file["ibstates/0/istate_index"]["basis_state_id"]
#
#        iter_coord_arr = numpy.zeros([num_segs, frames_per_iter, num_atoms, 3])
#        parent_coord_arr = numpy.zeros([num_segs, 1, num_atoms, 3])
        
        # Create an array to hold your data
        iter_data_arr = numpy.zeros((num_segs, frames_per_iter+1, num_atoms, data_dims))

        # Iterate over each segment
        for iseg in range(num_segs):
            print("  analyzing segment:",iseg)

            #Get the parent xml file (this is the hardest part)
            h5file = h5py.File("west.h5", "r")
            parent_seg_arr = h5file[self.h5iter_pattern.format(n_iter=n_iter)]["seg_index"]["parent_id"]
            bstate_id_arr = h5file["ibstates/0/istate_index"]["basis_state_id"]
            istate_type_arr = h5file["ibstates/0/istate_index"]["istate_type"]

            if int(parent_seg_arr[iseg]) < 0:
                parent_seg = int(parent_seg_arr[iseg])*-1
                parent_id = bstate_id_arr[parent_seg]
            else:
                parent_id = int(parent_seg_arr[iseg])
            
            h5 = h5io.WESTIterationFile(self.h5traj_pattern.format(n_iter=n_iter-1), "r")
            segment = Segment(n_iter=n_iter-1, seg_id=parent_id)

            try:
                h5.read_restart(segment)
                data = segment.data['iterh5/restart']
                d =io.BytesIO(data[:-1])
                with tarfile.open(fileobj=d, mode='r:gz') as t:
                    t.extractall(path=self.parent_pattern.format(n_iter=n_iter,n_seg=iseg))
                
                parent_file = self.parent_pattern.format(n_iter=n_iter,n_seg=iseg)+"/parent.xml"
            except ValueError as e:
                if segment.n_iter == 0:
                    print('Falling back to non-HDF5 files: ' + str(e))
                    if istate_type_arr[iseg] == 4:
                        start_ref = h5io.tostr(h5file['ibstates/0/istate_index']['basis_auxref'][iseg])
                        parent_file = self.start_pattern.format(auxref=start_ref)
                    else:
                        # Falling back to basis state files
                        basis_ref = h5io.tostr(h5file['ibstates/0/bstate_index']['auxref'][bstate_id_arr[iseg]])
                        parent_file = self.start_pattern.format(auxref=basis_ref)
                       

                else:
                    print(str(e))
        
       
            # The following is necessary for versions of h5py>3.3
            h5.close()
            
            parent_traj = mdtraj.load(parent_file, top=self.topfile)
            iter_traj = mdtraj.load(self.h5traj_pattern.format(n_iter=n_iter,n_seg=iseg), top=self.topfile)
            all_traj = mdtraj.join(parent_traj, iter_traj)
            #print(iter_traj)

            all_coords = all_traj.xyz[:,:,:]
            #print(all_coords.shape)
            #print(iter_data_arr.shape)

            iter_data_arr[iseg] = all_coords*10

        return iter_data_arr

class Crawler(WESTPACrawler):
    '''
    In this example, w_crawl works as follows:

    We supply the ``Crawler`` class, which handles writing data. The 
    Crawler specifies 3 methods: initialize, finalize, and process_iter_result.

    ``initialize`` is called only once--when w_crawl starts up. The job of 
    initialize is to create the output file (and HDF5 file).

    Like ``initialize``, ``finalize`` is also called only once--when w_crawl
    finishes calculations for all iterations. The job of ``finalize`` is to
    gracefully close the output file, preventing data corruption.

    The method ``process_iter_result`` is called once per weighted ensemble
    iteration. It takes the weighted ensemble iteration (n_iter) and the result
    of the calculations for an iteration (result) as arguments, and stores the
    data in the output file.

    The actual calculations are performed by the IterationProcessor class 
    defined above. In particular, the IterationProcessor.process_iteration 
    method performs the calculations; the return value of this method is passed
    to Crawler.process_iter_result.
    '''

    def initialize(self, iter_start, iter_stop):
        '''
        Create an HDF5 file for saving the data.  Change the file path to
        a location that is available to you. 
        '''
        self.output_file = h5io.WESTPAH5File('./crawl.h5', 'w')
        h5io.stamp_iter_range(self.output_file, iter_start, iter_stop)

    def finalize(self):
        self.output_file.close()

    def process_iter_result(self, n_iter, result):
        '''
        Save the result of the calculation in the output file.

        ----------
        Parameters
        ----------
        n_iter: (int) The index of the weighted ensemble iteration to which
          the data in ``result`` corresponds.
        result: (numpy.ndarray) In general this could be an arbitrary object
          returned by IterationProcessor.process_iteration; here it is a numpy
          array of the center of geometry.
        '''
        # Initialize/create the group for the specific iteration
        iter_group = self.output_file.require_iter_group(n_iter)

        iter_data_arr = result
        
        # Save datasets
        dataset = iter_group.create_dataset('example_data', 
                                            data=iter_data_arr, 
                                            scaleoffset=6, 
                                            compression=4,
                                            chunks=h5io.calc_chunksize(
                                                    iter_data_arr.shape,
                                                    iter_data_arr.dtype
                                                                       )
                                            )

# Entry point for w_crawl
iteration_processor = IterationProcessor()
def calculate(n_iter, iter_group):
    '''Picklable shim for iteration_processor.process_iteration()'''
    global iteration_processor 
    return iteration_processor.process_iteration(n_iter, iter_group)

crawler = Crawler()
