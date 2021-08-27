from __future__ import print_function, division
import numpy
from westpa.core.propagators import WESTPropagator
from westpa.core.systems import WESTSystem
from westpa.core.binning import RectilinearBinMapper
from westpa.core.binning import FuncBinMapper
from westpa.core.binning import RecursiveBinMapper

import logging
log = logging.getLogger('westpa.rc')

PI = numpy.pi
from numpy import *
pcoord_dtype = numpy.float32
#THESE ARE THE FOUR THINGS YOU SHOULD CHANGE
bintargetcount=4 #number of walkers per bin
numberofdim=2  # number of dimensions
binsperdim=[5,5]   # You will have prod(binsperdim)+numberofdim*(2+2*splitIsolated)+activetarget bins total
pcoordlength=101 # length of the pcoord
PCA=False       # choose to do principal component analysis
maxcap=[inf,inf]	#these are in the order of the dimensions left is first dimension and right is second dimension
mincap=[-inf,-inf]
targetstate=[None,None]    #enter boundaries for target state or None if there is no target state in that dimension
targetstatedirection=[-1]  #if your target state is meant to be greater that the starting pcoor use 1 or else use -1
activetarget=0		#if no target state make this zero
splitIsolated=1     #choose 1 if you want to split the most isolated walker (this will add an extra bin)

#########
def function_map(coords, mask, output):
	splittingrelevant=True
	varcoords=copy(coords)
	originalcoords=copy(coords)
	if PCA and len(output)>1:
		colavg=mean(coords, axis=0)
		for i in range(len(coords)):
			for j in range(len(coords[i])):
    	    			varcoords[i][j]=coords[i][j]-colavg[j]
		covcoords=cov(transpose(varcoords))
		eigval, eigvec=linalg.eigh(covcoords)
		eigvec=eigvec[:,argmax(absolute(eigvec),axis=1)]
		for i in range(len(eigvec)):
			if eigvec[i,i]<0:
				eigvec[:,i]=-1*eigvec[:,i]
		for i in range(numberofdim):
    			for j in range(len(output)):
    	    			coords[j][i]=dot(varcoords[j],eigvec[:,i])
	maxlist=[]
	minlist=[]
	difflist=[]
	flipdifflist=[]
	orderedcoords=copy(originalcoords)
	for n in range(numberofdim):
		try:
			extremabounds=loadtxt('binbounds.txt')
			currentmax=amax(extremabounds[:,n])
			currentmin=amin(extremabounds[:,n])
		except:
			currentmax=amax(coords[:,n])
			currentmin=amin(coords[:,n])
		if maxcap[n]<currentmax:
                	currentmax=maxcap[n]
		if mincap[n]>currentmin:
                	currentmin=mincap[n]
		maxlist.append(currentmax)
		minlist.append(currentmin)
		try:	
			temp=column_stack((orderedcoords[:,n],originalcoords[:,numberofdim]))
			temp=temp[temp[:,0].argsort()]
			for p in range(len(temp)):
                		if temp[p][1]==0:
                			temp[p][1]=10**-39
			fliptemp=flipud(temp)
			difflist.append(0)
			flipdifflist.append(0)	
			maxdiff=0
			flipmaxdiff=0
			for i in range(1,len(temp)-1):
				comprob=0
				flipcomprob=0
				j=i+1
				while j<len(temp):
					comprob=comprob+temp[j][1]
					flipcomprob=flipcomprob+fliptemp[j][1]
					j=j+1
				if temp[i][0]<maxcap[n] and temp[i][0]>mincap[n]:
					if (-log(comprob)+log(temp[i][1]))>maxdiff:
						difflist[n]=temp[i][0]
						maxdiff=-log(comprob)+log(temp[i][1])
				if fliptemp[i][0]<maxcap[n] and fliptemp[i][0]>mincap[n]:
					if (-log(flipcomprob)+log(fliptemp[i][1]))>flipmaxdiff:
						flipdifflist[n]=fliptemp[i][0]
						flipmaxdiff=-log(flipcomprob)+log(fliptemp[i][1])
		except:
			splittingrelevant=False
	for i in range(len(output)):
		holder=2*numberofdim
		for n in range(numberofdim):
			if (activetarget==1) and targetstate[n] is not None:
				if (originalcoords[i,n]*targetstatedirection) >= (targetstate[n]*targetstatedirection):
					holder=prod(binsperdim)+numberofdim*2
			if (holder==prod(binsperdim)+numberofdim*2):
				n=numberofdim
			elif coords[i,n]>=maxlist[n] or originalcoords[i,n]>=maxcap[n]:
				holder= 2*n
				n=numberofdim
			elif coords[i,n]<=minlist[n] or originalcoords[i,n]<=mincap[n]:
				holder =2*n+1
				n=numberofdim
			elif splittingrelevant and coords[i,n]==difflist[n] and splitIsolated==1:
				holder=prod(binsperdim)+numberofdim*2+2*n+activetarget
				n=numberofdim
			elif splittingrelevant and coords[i,n]==flipdifflist[n] and splitIsolated==1:
				holder=prod(binsperdim)+numberofdim*2+2*n+activetarget+1
				n=numberofdim
		if holder==2*numberofdim:
			for j in range(numberofdim):
				holder = holder + (digitize(coords[i][j],linspace(minlist[j],maxlist[j],binsperdim[j]+1))-1)*prod(binsperdim[0:j])
		output[i]=holder
	return output

class System(WESTSystem):
	def initialize(self):
		self.pcoord_ndim = numberofdim
		self.pcoord_len = pcoordlength
		self.pcoord_dtype = numpy.float32 
		self.bin_mapper = FuncBinMapper(function_map, prod(binsperdim)+numberofdim*(2+2*splitIsolated)+activetarget) #Changed binsperbin to binsperdim 
		self.bin_target_counts = numpy.empty((self.bin_mapper.nbins,), numpy.int_)
		self.bin_target_counts[...] = bintargetcount

