import h5py
import numpy
import mdtraj
import io
import tarfile
from westpa.core.h5io
from westpa.core.segment import Segment

frames_per_iter = 50
num_atoms = 4010

h5file = h5py.File("west.h5", "r")
num_segs = h5file["iterations/iter_00000001/seg_index"].shape[0]
parent_seg_arr = h5file["iterations/iter_00000001"]["seg_index"]["parent_id"]
bstate_id_arr = h5file["ibstates/0/istate_index"]["basis_state_id"]

iter_coord_arr = numpy.zeros([num_segs, frames_per_iter, num_atoms, 3])
parent_coord_arr = numpy.zeros([num_segs, 1, num_atoms, 3])

with h5py.File("traj_segs/iter_000001.h5", "r") as f:
    coords = f['coordinates'][:]
    coords = coords.reshape(num_segs, frames_per_iter, 4010, 3)
    for seg in range(0,num_segs):
        print("getting coords for segment: ", seg+1)
        iter_coord_arr[seg] = coords[seg]

h5 = h5io.WESTIterationFile("traj_segs/iter_000000.h5", "r")

for seg in range(0,num_segs):
    print("getting parent for segment: ", seg+1)

    if int(parent_seg_arr[seg]) < 0:
        parent_seg = int(parent_seg_arr[seg])*-1
        bstate_id = bstate_id_arr[parent_seg]

    segment = Segment(seg_id=bstate_id)

    h5.read_restart(segment)

    data = segment.data['iterh5/restart']

    d =io.BytesIO(data[:-1])  # remove tail protection
    with tarfile.open(fileobj=d, mode='r:gz') as t:
        t.extractall(path="./")

    parent_coords = mdtraj.load("parent.xml", top="bstate.pdb")
    parent_coord_arr[seg] = parent_coords.xyz[:]

all_coord_arr = numpy.concatenate((parent_coord_arr, iter_coord_arr), axis=1)
