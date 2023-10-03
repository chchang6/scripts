#!/usr/bin/env python
# find_env_diff.py: Parse two shell "env" text dumps, arrange envvar dicts for each,
#   and find which variables are different/missing.

import sys

if len(sys.argv) == 3:
   file1 = open(sys.argv[1], 'r')
   file2 = open(sys.argv[2], 'r')
else:
   sys.exit('Usage: find_env_diff.py old_env new_end')
data1 = file1.readlines()
file1.close()
data2 = file2.readlines()
file2.close()
envvars1 = {}
envvars2 = {}
for i in data1:
   t = i.strip().split('=',1)
   try:
      envvars1[t[0]] = t[1]
   except IndexError:
      envvars1[t[0]] = ''
for i in data2:
   t = i.strip().split('=',1)
   try:
      envvars2[t[0]] = t[1]
   except IndexError:
      envvars2[t[0]] = ''
# Look for cases where an environment 1 variable has been reset
for i in envvars1:
   if envvars2[i] != envvars1[i]:
      print '\nDifference in environments'
      print 'File1 variable ' + i + ' has value'
      print envvars1[i]
      print 'File2 variable ' + i + ' has value'
      print envvars2[i]
# Look for new environment variables in environment 2
for i in envvars2:
   if i not in envvars1:
      print '\nNew environment variable set: '
      print i + ' = ' + envvars2[i]
