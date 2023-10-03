#!/usr/bin/env python
import re, sys
import math

if len(sys.argv) < 3:
   print "Usage: parsegood.py <inputfile> <outputfile basename>"
   sys.exit()

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

RE1 = re.compile(r'Forward integration')
RE2 = re.compile(r'hmin')
namedict = {}
xdata = []
dydt = []
sortlist = []
for i in xrange(len(data)):
   if data[i].rstrip() == 'active species names':
      j = i + 2
      while j:
         try:
            temp = data[j].strip().split()
            namedict[temp[0]] = temp[2]
            j += 1
         except:
            j = 0
   elif RE1.search(data[i]):
      data[i] = data[i][24:]
      j = i
      while j:
         temp = data[j].strip().split()
         if temp[0] == 'x:':
            xdata.append(temp[2:])
            j += 1
         elif temp[0] == 'xdot:':
            dydt.append(temp[1:])
            j += 1
         elif RE2.search(temp[0]):
            j = 0
# Now sort compounds by RMS of gradients. Populate sortlist with tuples of (index, name, RMSgrad)
for i in namedict.keys():
   sumgrad = 0
   for j in xrange(len(dydt)):
      sumgrad += pow(float(dydt[j][int(i)]),2)
   RMSgrad = math.sqrt(sumgrad/len(dydt))
   sortlist.append( (i, namedict[i], RMSgrad) )
#   if i == '54' or i == '55': print (i, namedict[i], RMSgrad)
# Now bubble sort compounds by RMSgrad
i = 1
while i:
   numswaps = 0
   for j in xrange(len(sortlist)-1):
      temp1 = sortlist[j]
      comp1 = temp1[2]
      temp2 = sortlist[j+1]
      comp2 = temp2[2]
      if abs(comp2) < abs(comp1):
         sortlist[j] = temp2
         sortlist[j+1] = temp1
         numswaps += 1
   if numswaps == 0: break
# Now create two files, one with compound vs. RMS gradient, one with all data sorted by RMS gradient.
alldatafile = open(sys.argv[2]+'.data', 'w')
alldatafile.write('Data parsed by species, then cycle\n')
alldatafile.write('Cycle\tAmount\tGradient\n')
RMSdatafile = open(sys.argv[2]+'.RMS','w')
RMSdatafile.write('RMS gradients of each species over course of simulation\n')
RMSdatafile.write('Compound\tRMS gradient\tStarting gradient\tEnding gradient\n')
for i in sortlist:
   alldatafile.write(i[1])
   alldatafile.write('\n')
   RMSdatafile.write(i[1] + '\t' + str(i[2]) + '\t' + dydt[0][int(i[0])] + '\t' + dydt[-1][int(i[0])] + '\n')
   for j in xrange(len(xdata)):
      alldatafile.write('Cycle ' + str(j) + '\t')
      alldatafile.write(xdata[j][int(i[0])] + '\t')
      alldatafile.write('%5e' % float(dydt[j][int(i[0])]) + '\n')
alldatafile.close()
RMSdatafile.close()
