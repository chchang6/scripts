#!/usr/bin/env python
# Script to call hachoir-metadata on file, get creation data, rearrrange
#  to preferred filename format, then change filename.

import subprocess
import os, re, sys
import os.path

files = os.listdir('.') 
#for i in files:
for i in 'untitled.jpg':
   if i[-3:] == 'MOV':
      extension = '.MOV'
   elif i[-3:] == 'jpg':
      extension = '.jpg'
   else:
      continue
   if i[0:2] == 'CC': prefix = 'CiP'
   else: prefix = 'Zel'
   backslashed_filename = re.sub(' ', '\ ', i)  # Handles spaces
   backslashed_filename = re.sub('[(]', '\(', backslashed_filename) # Handles left parentheses
   backslashed_filename = re.sub('[)]', '\)', backslashed_filename) # Handles right parentheses
   x = subprocess.Popen('hachoir-metadata ' + backslashed_filename + ' | grep "Creation date"', shell=True, stdout=subprocess.PIPE).communicate()
   if x[0] != '':
      print i + ' --> ',
      x = x[0].lstrip('- Creation date: ')
      x = x.rstrip()
      (date, time) = x.split(' ')
      newdate = re.sub('-', '', date)
      newtime = re.sub(':', '', time)
      new_fileroot = prefix + newdate + '_' + newtime
      j = 0
      while True:
         j += 1
         if os.path.isfile(new_fileroot+extension):
            if j == 1:  # First time through
               new_fileroot += '01'
            elif j > 1 and j < 10:
               new_fileroot[-2:] = '0' + str(j)
            else: new_fileroot[-2:] = str(j)
         else:
            break
      print new_fileroot+extension
      os.rename(i, new_fileroot+extension)
