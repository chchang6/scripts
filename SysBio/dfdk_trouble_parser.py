#!/usr/bin/env python
import re
import math

file = open('test', 'r')
data = file.readlines()
file.close()

RE1 = re.compile(r'Forward integration')
namedict = {}
xdata = []
dydt = []
for i in data:
   if i.rstrip() == 'active species names':
      j = data.index(i) + 2
      while j:
         try:
            temp = data[j].strip().split()
            namedict[temp[0]] = temp[2]
            j += 1
         except:
            j = 0
   elif RE1.search(i):
      j = data.index(i) + 1
      while j:
         try:
            temp = data[j].strip().split()
            if temp[0] == 'x:':
               xdata.append(temp[2:])
               j += 1
            elif temp[0] == 'xdot:':
               dydt.append(temp[1:])
               j += 1
         except:
            j = 0
# Now sort compounds by RMS of gradients. Create new dictionary
RMSgraddict = {}
for i in namedict.keys():
   sumgrad = 0
   for j in xrange(len(xdata)):
      sumgrad += abs(float(xdata[j][int(i)-1]))
   RMSgrad = math.sqrt(sumgrad)
   RMSgraddict[RMSgrad] = i
# Now sort RMSgraddict by RMSgrad
RMSgradlist = []
for i in RMSgraddict.keys():
   RMSgradlist.append(i)
RMSgradlist.sort()
# Now create two files, one with compound vs. RMS gradient, one with all data sorted by RMS gradient.
alldatafile = open('data.txt', 'w')
RMSdatafile = open('compRMS.txt','w')
for i in RMSgradlist:
   index = RMSgraddict[i]
   alldatafile.write(namedict[index])
   alldatafile.write('\n')
   RMSdatafile.write(namedict[index] + '\t' + str(i) + '\n')
   for j in xrange(len(xdata)):
      alldatafile.write('Cycle ' + str(j) + '\t')
      alldatafile.write(xdata[j][int(index)] + '\t')
      alldatafile.write('%5e' % float(dydt[j][int(index)]) + '\n')
alldatafile.close()
RMSdatafile.close()
