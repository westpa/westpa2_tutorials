import scipy
import numpy
import re
from bootstrap import get_CR
import os

RunNums = 10
Rates = {}
MinVal = 10000    ### We replace all zeros with the smallest value measured

for run in range(1,RunNums+1) : 
   Rates[run] = []
   Times = []   # will be overwritten at each iteration, but that's okay
   RUN="{0:02}".format(run)
   FileIn = open("./data/rate_"+RUN+".dat")
   for line in FileIn.readlines() :
      Words = line.split()
      if (len(Words)>0) and (re.search("\d", Words[0])) :
         Times.append(Words[0]) 
         Rates[run].append(float(Words[1]))
         if (float(Words[1]) < MinVal) and (float(Words[1]) > 0)  : 
            MinVal = float(Words[1])
   FileIn.close()

if os.path.exists("./AvgRates_CR.dat"):
    os.remove("./AvgRates_CR.dat")

for i in range(len(Rates[1])) :
   print("time step", i+1, "/ ", len(Rates[1]))
   CurrData = []
   for run in range(1,RunNums+1) :
      CurrData.append(Rates[run][i])
   CurrAvg = scipy.average(CurrData)

   for j in range(len(CurrData)) :
      if CurrData[j] == 0 :  CurrData[j] = MinVal  ### We replace all zeros with the smallest value measured

   [CR_minval,CR_maxval] = get_CR(CurrData, 10000) ### 10000-fold Bayesian bootstrapping performed

   with open("AvgRates_CR.dat", "a") as fo:
       fo.write(str(Times[i]) + "\t" + str(CurrAvg) + "\t" + str(CR_maxval) + "\t" + str(CR_minval))
       fo.write("\n")
