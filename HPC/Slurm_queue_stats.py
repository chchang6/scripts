#!/usr/bin/env python

import subprocess

rawdata = subprocess.check_output(['squeue'], shell=True)
data = rawdata.split()
numj_v_user = {}
user_v_numt = {}
for i in range(8,len(data),8):
   queue = data[i+1]
   user = data[i+3]
   numnodes = int(data[i+6])
   if user not in numj_v_user:
      numj_v_user[user] = 1
   else:
      numj_v_user[user] += 1
   if user not in user_v_numt:
      user_v_numt[user] = {}
      user_v_numt[user][numnodes] = 1
   elif user in user_v_numt and numnodes not in user_v_numt[user]:
      user_v_numt[user][numnodes] = 1
   else:
      user_v_numt[user][numnodes] += 1

# Print reports
for i in numj_v_user:
   print 'User %10s has %5i jobs in the queue.' % (i, numj_v_user[i])
   for j in user_v_numt[i]:
      if user_v_numt[i][j] == 1:
         print '%5i job uses %4i nodes' % (user_v_numt[i][j], j)
      else:
         print '%5i jobs use %4i nodes' % (user_v_numt[i][j], j)
