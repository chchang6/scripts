#!/usr/bin/env python
# Find any files in directory not under version control, and add them
#   to tracking. Escape any space characters in filename.

import subprocess
import re
import time

x = subprocess.Popen('svn stat | grep ?', shell=True, stdout=subprocess.PIPE).communicate()
y = x[0].split('?')
for i in y:
   x = i.strip()
   if len(x) != 0:
      x = re.sub(' ', '\\ ', x)
      subprocess.Popen('svn add ' + x, shell=True)
      time.sleep(0.5)
