#!/usr/bin/python
# Python script to add atom indices of covariance matrix to
# top row and first column of CHARMM matrix output. Useful for
# import into CHARMM.
# Required input: covariance matrix file "covar.matrix"
#                 atom index list "indexlist", one index per line
# Output will be covar_indexed.matrix
import sys
atomfile = open('indexlist', 'r')
atomlist = atomfile.readlines()
numatoms = len(atomlist)
atomfile.close()
output = open('covar_indexed.matrix', 'w')
covarmatrix = open('covar.matrix', 'r')
a = 0
atomstring = ''
while a < numatoms:
   k = atomlist[a]
   j = k[0:-1] + ' '
   output.write(j)
   a += 1
output.write('\n')
b = 0
while b < numatoms:
   atom=atomlist[b]
   line=covarmatrix.readline()
   k = atom[0:-1] + ' '
   output.writelines([k,line])
   b += 1
covarmatrix.close()
