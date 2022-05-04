#!/usr/bin/python

import scipy
import random


################################################
############## DEFINING CI FUNCTION ############
################################################

def get_CI (List, Repeat) :

 if len(set(List)) == 1 :  	# NO CI if List has only identical elements
   return [0,0]

 else :
   AllMeans = []		# List of data(!) sample means for every bootstrap iteration
   N = len(List)                # Number of data points

   for i in range(Repeat) :	# Repeated bootstrap iterations
      CurrList = []		# Sample list
      for j in range(N) :
         CurrList.append(random.choice(List))
      AllMeans.append(scipy.average(CurrList))

   perc_min  = scipy.percentile(AllMeans,5)	# Minimum percentile defined over list of means 
   perc_max  = scipy.percentile(AllMeans,95) 	# Maximum percentile defined over list of means

   return [perc_min, perc_max]	# Confidence Interval is defined by min/max percentiles of sampling means

################################################





################################################
############## DEFINING CR FUNCTION ############
################################################

def get_CR (List, Repeat) :

 if len(set(List)) == 1 :  	# NO CR if List has only identical elements
   return [0,0]

 else :
   AllMeans = []		# List of model(!) sample means for every bootstrap iteration
   N = len(List)		# Number of data points

   for i in range(Repeat) :	# Repeated bootstrap iterations
      Rands = [0]		# Following Rubin et al. to get data probabilities from Dirichlet distrib.
      CurrAvg = 0
      for j in range(N-1) :
         Rands.append(random.random()) 
      Rands.append(1)
      Rands.sort()
      P=scipy.diff(Rands)	# List of random numbers that add to 1 and are used as data probabilities
      for j in range(N) :
         CurrAvg += P[j]*List[j]	# Sample mean
      AllMeans.append(CurrAvg)		
 
   AllMeans.sort()
   TotalProb = len(AllMeans)
   CumulProb = 0
   perc_min  = 0
   perc_max  = 0
   for m in AllMeans :	# Iterating through sorted means, identifying that mean at which a certain percentile of probs is reached
      CumulProb += 1
      if (CumulProb > 0.05*TotalProb) and (perc_min == 0) :
         perc_min = m   
      if (CumulProb > 0.95*TotalProb) and (perc_max == 0):
         perc_max = m

 return [perc_min, perc_max]		# Credibility Region is defined by min/max percentiles of sampling means 

#####################################################################
