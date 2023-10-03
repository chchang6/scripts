#!/usr/bin/env python

import re, sys

RE1 = re.compile('MO vectors')
RE2 = re.compile('Number of vectors in set 1')
RE3 = re.compile('Number of vectors in set 2')

def reorder(vec):
   newvec = []
   for i in QMMMorder:
      a = gasorder.index(i)
      endindex = gaspoints[a+1]
      startindex = gaspoints[a]
      newvec.extend(vec[startindex:endindex])
   return newvec

gasorder = ['Fe41','Fe42','Fe43','Fe44','N1','H2','C3','H4','C5','H6','H7','S8','C9','O10','N11','H12','C13',\
            'H14','C15','H16','H17','S18','C19','O20','N21','H22','C23','H24','C25','H26','H27','S28','C29',\
            'O30','N31','H32','C33','H34','C35','H36','H37','S38','C39','O40','S45','S46','S47','S48','H49',\
            'H50','H51','H52','H53','H54','H55','H56']
basisdict = {'Fe':34, 'S':22, 'O':18, 'N':18, 'C':14, 'H':5}
gaspoints = [0]
pointer = 0
for i in gasorder:
   element = re.sub('[0-9]+', '', i)
   pointer += basisdict[element]
   gaspoints.append(pointer)

QMMMorder = ['N1','H2','C3','H4','C5','H6','H7','S8','C9','O10','N11','H12','C13','H14','C15','H16','H17',\
             'S18','C19','O20','N21','H22','C23','H24','C25','H26','H27','S28','C29','O30','N31','H32','C33',\
             'H34','C35','H36','H37','S38','C39','O40','Fe41','Fe42','Fe43','Fe44','S45','S46','S47','S48','H49',\
             'H50','H51','H52','H53','H54','H55','H56']
# The following only needed for testing
QMMMpoints=[0]
pointer = 0
for i in QMMMorder:
   element = re.sub('[0-9]+', '', i)
   pointer += basisdict[element]
   QMMMpoints.append(pointer)
# End testing

infile = open(sys.argv[1], 'r')
data = infile.readlines()
infile.close()
outfile = open(sys.argv[2], 'w')
set = ''
read = False
i = 0
while i < len(data):
   if RE2.search(data[i]):
      outfile.write(data[i])
      numset1 = int(data[i].rstrip().split()[-1])
      if numset1 % 4 != 0:
         numrows1 = int(numset1/4) + 2  # Number of coefficient rows + MO label
      else:
         numrows1 = int(numset1/4) + 1  # Number of coefficient rows + MO label
   elif RE3.search(data[i]):
      outfile.write(data[i])
      numset2 = int(data[i].rstrip().split()[-1])
      if numset2 % 4 != 0:
         numrows2 = int(numset2/4) + 2  # Number of coefficient rows + MO label
      else:
         numrows2 = int(numset2/4) + 1  # Number of coefficient rows + MO label
   elif RE1.search(data[i]) and set == '':
      outfile.write(data[i])
      read = True
      set = 'alpha'
      i += 1
      continue
   elif RE1.search(data[i]) and set == 'alpha':
      outfile.write(data[i])
      read = True
      set = 'beta'
      i += 1
      continue
   elif read == True and set == 'alpha':
      for j in xrange(numset1):
         MO = data[i+j*numrows1]
         a = []
         for k in range(1,numrows1):
            if k < numrows1: limit = 4
            elif k == numrows1 and numset1 % 4 == 0: limit = 4
            elif k == numrows1 and numset1 % 4 != 0: limit = numset1 % 4
            else: raise ValueError('Problem with alpha conditional')
            for l in xrange(limit):
               a.append(data[i + j*numrows1 + k][l*20:(l+1)*20])
         b = reorder(a)
# For testing
#         if j == 1:
#            gas_testfile = open('gasalpha.test', 'w')
#            qmmm_testfile = open('qmmmalpha.test', 'w')
#            for k in xrange(len(a)):
#               gas_testfile.write(a[k])
#               gas_testfile.write('\n')
#               if (k+1) in gaspoints: gas_testfile.write('\n')
#            for k in xrange(len(a)):
#               qmmm_testfile.write(b[k])
#               qmmm_testfile.write('\n')
#               if (k+1) in QMMMpoints: qmmm_testfile.write('\n')
#            gas_testfile.close()
#            qmmm_testfile.close()
# End testing
         outfile.write(MO)
         for k in xrange(numrows1-1):
            if k < (numrows1-1): limit = 4
            else: limit = numset1 % 4
            for l in xrange(limit):
               outfile.write(b[k*4+l])
            outfile.write('\n')
      read = False
      i += numset1*numrows1
      continue
   elif read == True and set == 'beta':
      for j in xrange(numset2):
         MO = data[i+j*numrows2]
         a = []
         for k in range(1,numrows2):
            if k < numrows2: limit = 4
            elif k == numrows2 and numset2 % 4 == 0: limit = 4
            elif k == numrows2 and numset2 % 4 != 0: limit = numset2 % 4
            else: raise ValueError('Problem with beta conditional')
            for l in xrange(limit):
               a.append(data[i+j*numrows2+k][l*20:(l+1)*20])
         b = reorder(a)
# For testing
#         if j == 1:
#            gas_testfile = open('gasbeta.test', 'w')
#            qmmm_testfile = open('qmmmbeta.test', 'w')
#            for k in xrange(len(a)):
#               gas_testfile.write(a[k])
#               gas_testfile.write('\n')
#               if (k+1) in gaspoints: gas_testfile.write('\n')
#            for k in xrange(len(a)):
#               qmmm_testfile.write(b[k])
#               qmmm_testfile.write('\n')
#               if (k+1) in QMMMpoints: qmmm_testfile.write('\n')
#            gas_testfile.close()
#            qmmm_testfile.close()
# End testing
         outfile.write(MO)
         for k in xrange(numrows2-1):
            if k < (numrows2-1): limit = 4
            else: limit = numset2 % 4
            for l in xrange(limit):
               outfile.write(b[k*4+l])
            outfile.write('\n')
      read = False
      i += numset2*numrows2
      continue
   else:
      outfile.write(data[i])
   i += 1
outfile.close()
