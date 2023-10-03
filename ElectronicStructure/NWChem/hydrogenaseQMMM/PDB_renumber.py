#!/usr/bin/env python
import sys
file = open(sys.argv[1], 'r')    
data = file.readlines()         
file.close()
outfile = open(sys.argv[2], 'w') 
for i in xrange(len(data)):     
   x = data[i].split()          
   x[1] = i+1                   
   outfile.write('%4s%7i%c%-18s%8.3f%8.3f%8.3f%6.2f\n' % (x[0], x[1], ' ', x[2], float(x[3]), float(x[4]), float(x[5]), float(x[6])))
outfile.close()

