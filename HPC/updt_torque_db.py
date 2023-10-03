#!/usr/bin/env python
# Script to update compressed XML database based on last
#   entry. Run from admin2

import subprocess
import sys
import os
import stat
import re
import gzip
from shutil import copyfile
from datetime import date
from xml.etree import ElementTree as ET

torque_dir='/var/spool/torque/job_logs/'
dbfile='/scratch/cchang/MTL/job_database.xml'
## Copy existing gzip file as backup
copyfile(dbfile + '.gz', dbfile + '.gz.bak')
os.chmod(dbfile + '.gz.bak', stat.S_IRUSR)
subprocess.call('gunzip ' + dbfile + '.gz', shell=True)

RE1 = re.compile('<mtime>([0-9]{10})</mtime>')
RE2 = re.compile('[0-9]{8}')
RE3 = re.compile('<Jobinfo>')

# First find the latest job entry in the current XML file.
mtimes = subprocess.check_output(['grep', 'mtime', dbfile])
mtime_list = mtimes.split('\n')[0:-1]
for i in xrange(len(mtime_list)):
   mtime_list[i] = int(mtime_list[i].strip('mtime<>/'))
lasttime = max(mtime_list)
start_date = date.fromtimestamp(lasttime)
start_file = str(start_date.year) + '%02i' % start_date.month + str(start_date.day)

all_files = os.listdir(torque_dir)
uncomp_files = []
for i in all_files:
   if not RE2.match(i): continue
   t = date(int(i[0:4]), int(i[4:6]), int(i[6:]))
   if t >= start_date:
      uncomp_files.append(i)

datalist= ['<master>']
offset = int(subprocess.check_output(['grep', '-n', '<mtime>'+str(lasttime), torque_dir + start_file]).split(':')[0])
for i in uncomp_files:
   file = open(torque_dir + i, 'r')
   data = file.readlines()
   file.close()
   # First handle partial starting date data
   if i == start_file:
      starting_line = offset
   else:
      starting_line = 0
   # Clean up bad </JobId> tags and unallowed characters
   for j in range(starting_line, len(data)):
      data[j] = data[j].lstrip()
      data[j] = re.sub('</JobId>', '</Job_Id>', data[j])
      data[j] = re.sub('(&)(?=[^a])', '&amp;', data[j])
   # <job_script> data is particularly troublesome, parse ahead and correct bad XML characters
      if re.search('<job_script>', data[j]):
         k = 1
         while not re.search('</job_script>', data[j+k]):
            data[j+k] = re.sub('<', '&lt;', data[j+k])
            data[j+k] = re.sub('>', '&gt;', data[j+k])
            data[j+k] = re.sub('"', '&quot;', data[j+k])
            data[j+k] = re.sub('\'', '&apos;', data[j+k])
            k += 1
   # If this is the starting file, only want Jobs after offset. Find line number
   data_start = 0
   if i == start_file:
      for j in range(starting_line, len(data)):
         if RE3.search(data[j]):
            data_start = j; break
   datalist.extend(data[data_start:])
datalist.append('</master>\n')
# Having trouble parsing the plain appended-text product, so
#   will have to parse list into XML, then write it out.
newtree = ET.fromstringlist(datalist)
newjobs = newtree.iter('Jobinfo')
oldtree = ET.ElementTree()
oldtree.parse(dbfile)
oldroot = oldtree.getroot()
oldroot.extend(newjobs)

# Write out compressed XML file
outfile = gzip.open('job_database.xml.gz', 'wb')
oldtree.write(outfile, encoding="us-ascii", xml_declaration=True)
outfile.close()

# Write XML with new data
#outfile = open(dbfile, 'r+')
# Seek back to before '</master>' tag
#outfile.seek(-10, 2)
#outfile.write('\n')
# Write everything out
#for i in datalist:
#   outfile.write(i)
#outfile.close()
# Pack db file up
#outgzfile = open(dbfile + '.gz', 'w')
#subprocess.call(['gzip', '-c', dbfile], stdout=outgzfile)
#outgzfile.close()

