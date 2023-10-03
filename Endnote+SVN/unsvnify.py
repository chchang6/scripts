#!/usr/bin/env python
#
# Script to "un-SVN" directories by removing all .svn folders.

import subprocess
import re, sys

x = subprocess.Popen('find . -name ".svn"', shell=True, stdout=subprocess.PIPE).communicate()
y = re.split('\n', x[0])
print 'Removing files...'
for i in y:
   x = i.strip()
   x = re.sub(' ', '\\ ', x)
   if len(x) != 0:
      subprocess.Popen('rm -rf ' + x + '\n', shell=True).wait()

