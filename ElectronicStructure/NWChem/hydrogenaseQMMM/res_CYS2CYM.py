#!/usr/bin/env python

import sys, re

cyslist = [34, 46, 49, 62, 98, 101, 107, 147, 150, 153, 200, 157, 190, 193, 196, 300, 355, 499, 503]

infile = open(sys.argv[1], 'r')
data = infile.readlines()
infile.close()

outfile = open(sys.argv[2], 'w')
for i in xrange(len(data)):
   try:
      if int(data[i][22:26]) in cyslist:
          data[i] = re.sub('CYS','CYM', data[i])
      outfile.write(data[i])
   except:
      outfile.write(data[i])
outfile.close()
