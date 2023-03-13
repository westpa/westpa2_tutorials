import h5py
import numpy

# this is the final iteration number from your simulation
li=2

# this is your file from w_crawl
crawlh5 = h5py.File("coord.h5", "r")

# this is your main simulation h5 file
westh5 = h5py.File("west.h5", "a")

# loop though all iterations and copy one at a time into the main h5file
for i in range(1,li+1):

    # this is the location and name of the new data from your w_crawl h5 file
    crawlh5_string = 'iterations/iter_'+str(i).zfill(8)+'/coord'

    # this is the destination in the west h5 file to place your new data,
    # you can change the name if you want but make sure to put it in auxdata
    westh5_string = 'iterations/iter_'+str(i).zfill(8)+'/auxdata/coord'

    # define the source dset of w_crawl output h5 file
    copy_arr = crawlh5[crawlh5_string]

    # copy into destination path of west.h5
    # warn the user if it exists and give them a chance to exit
    try:
        westh5.create_dataset(westh5_string, data=copy_arr)
        print('saved data for iteration %s' % i)
    except Exception:
        warning = input('Dataset already exists in iteration %s! Overwrite? (y/n)' % i)
        if warning == "y":
            westh5[westh5_string][...] = copy_arr
            print('saved data for iteration %s' % i)
        else:
            print('crawlh5 data not saved. Exiting...')
            exit

# close the files (to avoid data corruption)
crawlh5.close()
westh5.close()
