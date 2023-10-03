#!/usr/bin/env python
import re
import math

file = open('glycolysis5', 'r')
data = file.readlines()
file.close()

RE1 = re.compile(r'Forward integration')
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
         print j
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
# Now sort compounds by RMS of gradients. Populate sortlist with tuples of (index, name, RMSgrad)
print xdata[0]
print xdata[1]
for i in namedict.keys():
   sumgrad = 0
   for j in xrange(len(xdata)):
      sumgrad += pow(float(xdata[j][int(i)]),2)
   RMSgrad = math.sqrt(sumgrad)
   sortlist.append( (i, namedict[i], RMSgrad) )
   if i == '54' or i == '55': print (i, namedict[i], RMSgrad)
# Now bubble sort by RMSgrad
i = 1
while i:
   numswaps = 0
   for j in xrange(len(sortlist)-1):
      temp1 = sortlist[j]
      comp1 = temp1[2]
      temp2 = sortlist[j+1]
      comp2 = temp2[2]
      if comp2 < comp1:
         sortlist[j] = temp2
         sortlist[j+1] = temp1
         numswaps += 1
   if numswaps == 0: break
# Now create two files, one with compound vs. RMS gradient, one with all data sorted by RMS gradient.
alldatafile = open('data.txt', 'w')
RMSdatafile = open('compRMS.txt','w')
mingradfile = open('compminG.txt', 'w')
for i in sortlist:
   alldatafile.write(i[1])
   alldatafile.write('\n')
   RMSdatafile.write(i[1] + '\t' + str(i[2]) + '\n')
   mingradfile.write(i[1] + '\t' + dydt[1][int(i[0])] + '\n')
   for j in xrange(len(xdata)):
      alldatafile.write('Cycle ' + str(j) + '\t')
      alldatafile.write(xdata[j][int(i[0])] + '\t')
      alldatafile.write('%5e' % float(dydt[j][int(i[0])]) + '\n')
alldatafile.close()
RMSdatafile.close()
mingradfile.close()
