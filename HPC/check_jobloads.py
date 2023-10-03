#!/usr/bin/python
import os
import sys
try:
   x='qstat -n ' + sys.argv[1] + ' > temp'
except IndexError:
   print "Usage: check_jobloads.py jobid"
else:
   os.system(x)
   sys.stdin=open('temp', 'r')
   data=sys.stdin.readlines()
   queue = data[5].split()[2]
   print queue
   data = data[6:]
   test = str('')
   for x in data:
      y=x.strip(' \n')
      test = test + y
   z=test.split("+")
   i = 0
   if queue == 'Std':
      mod = 2
   elif queue == 'Std8':
      mod = 8
   elif queue == 'Ib':
      mod = 4
   else:
      assert AttributeError, 'Set up another queue in this script!'
   for x in z:
      if i % mod == 0:
         y = "checknode " + x[:-2] + " | grep Load"
         print x[:-2]
         os.system(y)
      i = i + 1
   sys.stdin.close()
   os.system("rm temp")
