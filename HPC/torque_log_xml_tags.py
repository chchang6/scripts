#!/usr/bin/env python
# Script to identify XML start tags present in a file, and count them

import re, os

RE1 = re.compile('<[^/>]+?>')
RE2a = re.compile('<job_script>')
RE2b = re.compile('</job_script>')
RE3 = re.compile('[0-9]{8}')
datadict = {}

torque_dir = '/var/spool/torque/job_logs/'

files = os.listdir(torque_dir)

for i in files:
   if not RE3.match(i): continue
   else:
      file = open(torque_dir + i, 'r')
      data = file.readlines()
      file.close()
      in_script = False
      for j in data:
         if RE2a.search(j): in_script = True
         elif RE2b.search(j): in_script = False
         t = RE1.search(j)
         if t and in_script == False:
            if t.group(0) not in datadict:
               datadict[t.group(0)] = 1
            else:
               datadict[t.group(0)] += 1

unique_values = sorted(list(set(datadict.values())))

for i in unique_values:
   for j in datadict:
      if datadict[j] == i:
         print '%s\t%i' % (j, datadict[j])

