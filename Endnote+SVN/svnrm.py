#!/usr/bin/env python
# If "!" is in First column of svn stat output, a file was removed without
#   syncing the database. The following just cleans those entries up.
#   Filenames with spaces need to have an escape backslash inserted before
#   sending to svn delete.

import subprocess
import re
import time

x = subprocess.Popen('svn stat | grep !', shell=True, stdout=subprocess.PIPE).communicate()
y = x[0].split('!')
for i in y:
   x = i.strip()
   if len(x) != 0:
      x = re.sub(' ', '\\ ', x)
      subprocess.Popen('svn delete ' + x, shell=True)
      time.sleep(0.5)
