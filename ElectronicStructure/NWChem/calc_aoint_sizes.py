#!/usr/bin/env python

from numpy import average, amax
import glob, os

data = glob.glob('/scratch/chchang/HRHERTFN8g6tWCqK_1b/scr/*.aoints.*')
sizes = []
for i in data:
   temp = os.stat(i).st_size
   sizes.append(float(temp))
BYTE_TO_GB=pow(1024,3)
print 'Average AO integral file size is %8.5f GB' % (average(sizes)/BYTE_TO_GB)
print 'Maximum AO integral file size is %8.5f GB' % (amax(sizes)/BYTE_TO_GB)

