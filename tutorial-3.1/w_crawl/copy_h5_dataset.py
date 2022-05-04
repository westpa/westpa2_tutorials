import h5py
import numpy

file1 = h5py.File("crawl.h5", "r")
file2 = h5py.File("west.h5", "a")

for i in range(1,1001):
    f1string = 'iterations/iter_'+str(i).zfill(8)+'/example_data'
    f2string = 'iterations/iter_'+str(i).zfill(8)+'/auxdata/example_data'
    print(f2string)
    copy_arr = file1[f1string]
    file2.create_dataset(f2string, data=copy_arr)

file1.close()
file2.close()
