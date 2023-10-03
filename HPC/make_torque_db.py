#!/usr/bin/env python
# Script to parse torque logs of PBS jobs de novo, and dump
#   to compressed XML database

import os, re
import optparse
import tarfile
import gzip
from sys import exit
from time import strftime
from datetime import date
from xml.etree import ElementTree as ET

class Job:
   def set_walltime(self, seconds):
      self.walltime = seconds
   def get_walltime(self):
      return self.walltime
   def set_id(self, id):
      self.id = id
   def get_id(self):
      return self.id
   def set_nodecount(self, count):
      self.nodecount = count
   def get_nodecount(self):
      return self.nodecount
   def set_jobscript(self, stringy):
      self.jobscript = stringy
   def get_jobscript(self):
      return self.jobscript

def clean_text(stringlist):
   # Clean up bad </JobId> tags and unallowed characters
   # First make sure </job_script> is on its own line, otherwise substitutions may fail
   i = 0
   while i < len(stringlist):
      t = stringlist[i]
      if re.search('</job_script>', t) and not re.match('</job_script>', t):
         t2 = re.search('(.+)</job_script>', t).group(1)
         stringlist.insert(i, t2)
         t = '</job_script>'
         stringlist[i+1] = t
      i += 1
   # Now substitute problems
   for i in xrange(len(stringlist)):
      t = stringlist[i]
      t = t.lstrip()
      t = re.sub('</JobId>', '</Job_Id>', t)
      stringlist[i] = t
      # <job_script> content is particularly troublesome, parse ahead and correct bad XML characters
      if re.search('<job_script>', t):
         j = 1
         while not re.search('</job_script>', stringlist[i+j]):
            t2 = stringlist[i+j]
            t2 = re.sub('(&)(?=[^a])', '&amp;', t2)
            t2 = re.sub('<', '&lt;', t2)
            t2 = re.sub('>', '&gt;', t2)
            t2 = re.sub('"', '&quot;', t2)
            t2 = re.sub('\'', '&apos;', t2)
            stringlist[i+j] = t2
            j += 1
   return

def make_datalist_uncomp(dir,filelist):
   datalist = []
   for i in filelist:
      print 'Cleaning up ' + i
      file = open(dir + i)
      data = file.readlines()
      file.close()
      clean_text(data)
      datalist.extend(data)
   return datalist

def make_datalist_compressed(dir, filelist):
   datalist = []
   for i in filelist:
      file = tarfile.open(dir + '/' + i, 'r:gz')
      logs = file.getnames()
      for j in logs:
         t = date(int(j[0:4]), int(j[4:6]), int(j[6:]))
         if t >= start_date and t <= end_date:
            print 'Cleaning up ' + j
            logfile = file.extractfile(j)
            data = logfile.readlines()
            logfile.close()
            clean_text(data)
            datalist.extend(data)
      file.close()
   return datalist

# Diagnostic expressions in job scripts for different executables
#signatures = { 'vasp': (re.compile('pylada', re.I), re.compile('vasp', re.I)), 
#               'gaussian': re.compile('g09'),
#               'amber': re.compile('sander', re.I),
#               'wrf': re.compile('wrf', re.I),
#               'nwchem': re.compile('nwchem', re.I)
#              }
parser = optparse.OptionParser()
parser.add_option('-s', '--start-date', action='store', type='string', dest='start_date_string', help='Start date in format YYYY-MM-DD')
parser.set_defaults(end_date_string=strftime('%Y-%m-%d'))
parser.add_option('-e', '--end-date', action='store', type='string', dest='end_date_string', help='End date in format YYYY-MM-DD')
(options, args) = parser.parse_args()
if not options.start_date_string:
   parser.print_help()
   exit()

torque_dir='/scratch/cchang/job_logs/'
torque_compressed_dir='/scratch/cchang/job_logs/old'

t = options.start_date_string.split('-')
start_year = int(t[0])
start_month = int(t[1])
start_day = int(t[2])
start_date = date(start_year, start_month, start_day)
t = options.end_date_string.split('-')
end_year = int(t[0])
end_month = int(t[1])
end_day = int(t[2])
end_date = date(end_year, end_month, end_day)

# Get uncompressed file list first, then determine if start date requires
#   going into compressed files.
uncompr_file_list = os.listdir(torque_dir)
# Luckily, lexical sort order also will sort these by date
uncompr_file_list = sorted(uncompr_file_list)
oldest = date(int(uncompr_file_list[0][0:4]), int(uncompr_file_list[0][4:6]), int(uncompr_file_list[0][6:]))
#oldest = date(2100, 12, 31)
#for i in uncompr_file_list:
#   if not re.match('[0-9]{8}', i): continue
#   t = date(int(i[0:4]), int(i[4:6]), int(i[6:]))
#   if t >= start_date and t <= end_date:
#      if t < oldest: oldest = t
# If start_date is older than the oldest uncompressed file, then must need compressed files
if start_date < oldest:
   compr_file_list = os.listdir(torque_compressed_dir)
   compressed_files = []
   for i in compr_file_list:
      if not re.match('[0-9]{6}.tar.gz', i) and not re.match('[0-9]{6}.tgz', i): continue
      if start_date.year <= int(i[0:4]):
         if start_date.month <= int(i[4:6]):
            compressed_files.append(i)
# If end_date is after the oldest uncompressed file, then will need uncompressed files
if end_date >= oldest:
   uncomp_files = []
   for i in uncompr_file_list:
      if not re.match('[0-9]{8}', i): continue
      t = date(int(i[0:4]), int(i[4:6]), int(i[6:]))
      if t >= start_date and t <= end_date:
         uncomp_files.append(i)
uncomp_files = sorted(uncomp_files)

datalist= ['<master>\n']
# First process compressed files
try:
   datalist.extend(make_datalist_compressed(torque_compressed_dir, compressed_files))
except NameError:
   print 'Don\'t need compressed files'

# Then uncompressed 
datalist.extend(make_datalist_uncomp(torque_dir, uncomp_files))
#try:
#   datalist.extend(make_datalist_uncomp(torque_dir, uncomp_files))
#except NameError:
#   print 'Don\'t need uncompressed files'

datalist.append('</master>')

# Parse XML
tree = ET.fromstringlist(datalist)
#jobs = tree.iter('Jobinfo')
#datadict = {}
#for i in jobs:
#   if i.find('resources_used') == None:
#      print i.find('Job_Id').text + ' failed!'
#   else:
#   job = Job()
#   job.set_id(re.sub('.admin[0-9]', '', i.find('Job_Id').text))
#   job.set_walltime(int(i.find('resources_used/walltime').text))
#   job.set_nodecount(int(i.find('Resource_List/nodect').text))
#   job.set_jobscript(i.find('job_script').text)
#   datadict[job.get_id()] = job

# Write out compressed XML file
outfile = gzip.open('test_db.xml.gz', 'wb')
#outfile = gzip.open('job_database.xml.gz', 'wb')
fulltree = ET.ElementTree(tree)
fulltree.write(outfile, encoding="us-ascii", xml_declaration=True)
outfile.close()
