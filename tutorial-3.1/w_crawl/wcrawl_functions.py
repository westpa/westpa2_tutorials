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
        # find the number of segments in the iteration at hand
        print("starting iteration", n_iter)
        num_segs = iter_group['seg_index'].shape[0]

        parent_iter = n_iter-1

        # change the following to match your system, not that if you only need a single
        # value per frame, you don't need the num_atoms index and can instead just do:
        #
        #     iter_data_arr = numpy.zeros((num_segs, frames_per_iter, data_dims))
        #
        # the following is more of a special case for coordinate extraction

        frames_per_iter = 3 # remember this is +1 since the bstate is always included first
        num_atoms = 2 # we'll just save the coordinates for Na+ and Cl-
        data_dims = 3 # since each atom has an x, y and z coordinate

        # create an array to hold your data
        iter_data_arr = numpy.zeros((num_segs, frames_per_iter, num_atoms, data_dims))

        # iterate over each segment
        for iseg in range(num_segs):
            print("analyzing segment:", iseg)

            # find out which segment from parent_iter is the parent;
            # in general, don't change anything in this section.
            h5file = h5py.File("west.h5", "r")
            parent_seg_arr = iter_group['seg_index']['parent_id']
            bstate_id_arr = h5file['ibstates/0/istate_index']['basis_state_id']
            istate_type_arr = h5file['ibstates/0/istate_index']['istate_type']

            if int(parent_seg_arr[iseg]) < 0:
                parent_seg = int(parent_seg_arr[iseg])*-1
                parent_id = bstate_id_arr[parent_seg]
                parent_iter = 0 # this means that the parent is a bstate
            else:
                parent_id = int(parent_seg_arr[iseg])
            
            parent_iter_h5_filepath = "traj_segs/iter_"+str(int(parent_iter)).zfill(6)+".h5"
            parent_pointer = h5py.File(parent_iter_h5_filepath)['pointer'][:,1]
            parent_where = numpy.where(parent_pointer == parent_id)
            parent_traj = mdtraj.load(parent_iter_h5_filepath)[parent_where]

            # this is where you'll want to change things to suit your analysis,
            # here, the parent_traj is used to get coordinates, but you could
            # do any mdtraj or mdanalysis-related calculation here once you
            # have the trajectory selected.
            parent_coord_array = parent_traj.xyz[-1,:2,:] # the :2 index just gets the coordinates for Na+ and Cl-

            # don't change the following block
            iter_h5_filepath = "traj_segs/iter_"+str(int(n_iter)).zfill(6)+".h5"
            pointer = h5py.File(iter_h5_filepath)['pointer'][:,1]
            where = numpy.where(pointer == iseg)
            iter_traj = mdtraj.load(iter_h5_filepath)[where]

            # this will be the same as above but run on the "main"
            # trajectory frames instead of the parents.
            iter_coord_array = iter_traj.xyz[:,:2,:] # the :2 index just gets the coordinates for Na+ and Cl-

            # combine the parent and main iter trajectory datasets, not that I don't
            # concatenate the trajectories themeselves, but you could technically do that.
            # (I don't do that here becasue I think this is safer...)
            coord_array = numpy.concatenate((parent_coord_array.reshape(1,2,3), iter_coord_array), axis=0) 
 
            coord_array *= 10 # convert coordinates from nm to angstroms

            # this will loop through iter_data_arr and put our data where it needs to be,
            # you shouldn't need to change this.
            for num, val in enumerate(coord_array):
                iter_data_arr[iseg, num] = val

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
        # name your new hdf5 data file here
        self.output_file = h5io.WESTPAH5File('./coord.h5', 'w')
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
        
        # name your new hdf5 dataset here
        dataset = iter_group.create_dataset('coord', 
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
