#!/usr/bin/env python
# Script to remove duplicate entries from XML jobs database.

import gzip
from xml.etree import ElementTree as ET
from shutil import copyfile
from os import remove
from os.path import exists
import sys

# Parse XML
if not exists('job_database.xml.gz'):
   sys.exit('No input file job_database.xml.gz exists!')
else:
   file = gzip.open('job_database.xml.gz', 'rb')
if exists('job_database.xml.gz.bak'):
   file.close()
   sys.exit('Backup file job_database.xml.gz.bak already exists!')
else:
   copyfile('job_database.xml.gz', 'job_database.xml.gz.bak')
root = ET.ElementTree().parse(file)
file.close()
existing_jobs = root.iter('Jobinfo')
jobids = []
for i in existing_jobs:
   t = i.find('Job_Id').text
   if t in jobids:
      print 'Found redundant job ' + str(t) + '; removing'
      root.remove(i)
   else:
      jobids.append(t)

# Double check jobids for redundant entries
print 'Checking for redundant jobs after clean up'
for i in xrange(len(jobids)):
   if jobids.index(jobids[i]) < i:
      print 'Uh oh, redundant job ' + jobids[i]

# Write out compressed XML file
remove('job_database.xml.gz')
outfile = gzip.open('job_database.xml.gz', 'wb')
tree = ET.ElementTree()
tree._setroot(root)
tree.write(outfile, encoding="us-ascii", xml_declaration=True)
outfile.write('\n')
outfile.close()
