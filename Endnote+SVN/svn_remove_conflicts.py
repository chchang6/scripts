#!/usr/bin/env python
# Find modified files with revisions in directory tree.
#   Delete them, then pull from remote.

import subprocess
import re
import os

x = subprocess.Popen('svn stat | grep \'^M\'', shell=True, stdout=subprocess.PIPE).communicate()
y = re.split('\nM', x[0])
if re.match('^M', y[0]): y[0] = y[0][1:]
print 'Resolving conflicts...'
for i in y:
   x = i.strip()
   r = x + '.r*'
   if len(x) != 0:
      print 'Deleting ' + x
      os.remove(x)
      print 'Deleting revisions'
      os.remove(r)
print 'Updating local repository with remote files.'
subprocess.Popen('svn up', shell=True)
