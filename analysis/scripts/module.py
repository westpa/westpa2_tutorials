#!/usr/bin/env python

import numpy

def load_auxdata(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/COG']
    auxgroup2 = iter_group['auxdata/COM']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset
