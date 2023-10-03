#!/usr/bin/env python
# Script to undo trivial changes made when Endnote opens files without modification,
#   such as occurs when browsing a library.

import subprocess
import re, sys

if sys.argv[1] == 'revert':
   x = subprocess.Popen('svn stat | grep \'^M\'', shell=True, stdout=subprocess.PIPE).communicate()
   y = re.split('\nM', x[0])
   if re.match('^M', y[0]): y[0] = y[0][1:]
   print 'Reverting files...'
   for i in y:
      x = i.strip()
      x = re.sub(' ', '\\ ', x)
      if len(x) != 0:
         subprocess.Popen('svn revert ' + x + '\n', shell=True)
elif sys.argv[1] == 'delete':
   x = subprocess.Popen('svn stat | grep \'^M\'', shell=True, stdout=subprocess.PIPE).communicate()
   y = re.split('\nM', x[0])
   if re.match('^M', y[0]): y[0] = y[0][1:]
   print 'Reverting files...'
   for i in y:
      x = i.strip()
      x = re.sub(' ', '\\ ', x)
      if len(x) != 0:
         subprocess.Popen('rm -f ' + x + '\n', shell=True)

