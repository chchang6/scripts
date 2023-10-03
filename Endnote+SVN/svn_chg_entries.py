#!/usr/bin/env python
# Changing remotes.
# Find files with remote tracking entries on old server.
#   For each, backup, then change all old entries ('lester") to target ones ('scctools')
#   Script svn_rm_entriesbak.py then removes the backups once updates are verified.

import subprocess
import re, shutil, os, stat

x = subprocess.Popen('find . -name entries', shell=True, stdout=subprocess.PIPE).communicate()
y = x[0].split('\n')
for i in y:
   if len(i) != 0:
      x = re.sub(' ', '\ ', i)
      os.chmod(i, 0644) 
      backup = i + '.bak'
      shutil.copyfile(i, backup)
      file = open(i,'r')
      data = file.readlines()
      file.close()
      file = open(i,'w')
      for j in xrange(len(data)):
         file.write(re.sub('lester.domain.name/uhome', 'scctools.domain.name/home', data[j]))
      file.close()
      os.chmod(i, 0444)
   print 'Done with ' + i
