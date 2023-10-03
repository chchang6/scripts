#!/usr/bin/env python
# Script to parse torque logs of PBS jobs in various ways

import os, re
import optparse
#import tarfile
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

# Diagnostic expressions in job scripts for different executables
signatures = { 'vasp': (re.compile('pylada', re.I), re.compile('vasp', re.I)), 
               'gaussian': re.compile('g09'),
               'amber': re.compile('sander', re.I),
               'wrf': re.compile('wrf', re.I),
               'nwchem': re.compile('nwchem', re.I)
              }
parser = optparse.OptionParser()
parser.add_option('-s', '--start-date', action='store', type='string', dest='start_date_string', help='Start date in format YYYY-MM-DD')
parser.set_defaults(end_date_string=strftime('%Y-%m-%d'))
parser.add_option('-e', '--end-date', action='store', type='string', dest='end_date_string', help='End date in format YYYY-MM-DD')
(options, args) = parser.parse_args()

torque_dir='/var/spool/torque/job_logs/'
torque_compressed_dir='/var/spool/torque/job_logs/old'

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

uncompr_file_list = os.listdir(torque_dir)
compr_file_list = os.listdir(torque_compressed_dir)
oldest = date(2100, 12, 31)
uncomp_files = []
compressed_files = []
for i in uncompr_file_list:
   if not re.match('[0-9]{8}', i): continue
   t = date(int(i[0:4]), int(i[4:6]), int(i[6:]))
   if t >= start_date and t <= end_date:
      uncomp_files.append(i)
for i in compr_file_list:
   if not re.match('[0-9]{6}.tar.gz', i) and not re.match('[0-9]{6}.tgz', i): continue
   if start_date.year <= int(i[0:4]):
      if start_date.month <= int(i[4:6]):
         compressed_files.append(i)

# First the uncompressed files
datalist= ['<master>\n']
for i in uncomp_files:
   file = open(torque_dir + i)
   data = file.readlines()
   file.close()
   # Clean up bad </JobId> tags and unallowed characters
   for j in xrange(len(data)):
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
   datalist.extend(data)
datalist.append('</master>')

# Here will go the data from compressed tarballs

# Parse XML
tree = ET.fromstringlist(datalist)
jobs = tree.iter('Jobinfo')
datadict = {}
for i in jobs:
   if i.find('resources_used') == None:
      print i.find('Job_Id').text + ' failed!'
   else:
      job = Job()
      job.set_id(re.sub('.admin[0-9]', '', i.find('Job_Id').text))
      job.set_walltime(int(i.find('resources_used/walltime').text))
      job.set_nodecount(int(i.find('Resource_List/nodect').text))
      job.set_jobscript(i.find('job_script').text)
      datadict[job.get_id()] = job

# Change below for each analysis
vasp_nodehours = 0
gaussian_nodehours = 0
amber_nodehours = 0
wrf_nodehours = 0
nwchem_nodehours = 0

for i in datadict:
   t = datadict[i].get_jobscript()
   if signatures['vasp'][0].search(t) or signatures['vasp'][1].search(t):
      vasp_nodehours += float(datadict[i].get_walltime())/3600. * datadict[i].get_nodecount()
   elif signatures['gaussian'].search(t):
      gaussian_nodehours += float(datadict[i].get_walltime())/3600. * datadict[i].get_nodecount()
   elif signatures['amber'].search(t):
      amber_nodehours += float(datadict[i].get_walltime())/3600. * datadict[i].get_nodecount()
   elif signatures['wrf'].search(t):
      wrf_nodehours += float(datadict[i].get_walltime())/3600. * datadict[i].get_nodecount()
   elif signatures['nwchem'].search(t):
      nwchem_nodehours += float(datadict[i].get_walltime())/3600. * datadict[i].get_nodecount()

print 'Vasp node hours used between ' + options.start_date_string + ' and ' + options.end_date_string + ': ',
print vasp_nodehours
print 'Gaussian node hours used between ' + options.start_date_string + ' and ' + options.end_date_string + ': ',
print gaussian_nodehours
print 'Amber node hours used between ' + options.start_date_string + ' and ' + options.end_date_string + ': ',
print amber_nodehours
print 'WRF node hours used between ' + options.start_date_string + ' and ' + options.end_date_string + ': ',
print wrf_nodehours
print 'NWChem node hours used between ' + options.start_date_string + ' and ' + options.end_date_string + ': ',
print nwchem_nodehours
