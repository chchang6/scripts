#!/usr/bin/env python
# Remove any "entries.bak" files in file tree.

import subprocess
import os, re

x = subprocess.Popen('find . -name entries.bak', shell=True, stdout=subprocess.PIPE).communicate()
y = x[0].split('\n')
for i in y:
   if len(i) != 0:
      x = re.sub(' ', '\ ', i)
      os.remove(i)
   print 'Removed ' + i
