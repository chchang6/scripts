#!/usr/bin/env python
# Script to parse torque logs of PBS jobs de novo, and search for
#   to module loads of selected modules

import os, re
import optparse
import tarfile
import gzip
from sys import exit
from datetime import date
from time import strftime

def count_loads_uncomp(dir, filelist, moduleRE):
   count = 0
   for i in filelist:
      file = open(dir + i)
      data = file.readlines()
      file.close()
      for i in data:
         if moduleRE.search(i): count += 1
   return count

def count_loads_compressed(dir, filelist, moduleRE):
   count = 0
   for i in filelist:
      file = tarfile.open(dir + '/' + i, 'r:gz')
      logs = file.getnames()
      for j in logs:
         # Eliminate weird little binary file with just month
         if re.match('201[4-9][0-9]{2}', j[-6:]): continue
         t = date(int(j[-8:-4]), int(j[-4:-2]), int(j[-2:]))
         if t >= start_date and t <= end_date:
            logfile = file.extractfile(j)
            data = logfile.readlines()
            logfile.close()
            for k in data:
               if moduleRE.search(k): count += 1
      file.close()
   return count

parser = optparse.OptionParser()
parser.add_option('-s', '--start-date', action='store', type='string', dest='start_date_string', help='Start date in format YYYY-MM-DD')
parser.set_defaults(end_date_string=strftime('%Y-%m-%d'))
parser.add_option('-e', '--end-date', action='store', type='string', dest='end_date_string', help='End date in format YYYY-MM-DD')
parser.add_option('-m', '--module', action='store', type='string', dest='module_target', help='Name of module in format name/version[/toolchain]')
(options, args) = parser.parse_args()
if not options.start_date_string:
   parser.print_help()
   exit()

# Convert argv[1] slashes and convert to RE
target_string = re.sub('/', '\/', options.module_target)
RE1 = re.compile(target_string)

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
# Test
#print start_date
#print end_date
#exit()

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

# First process compressed files
try:
   compressed_count = count_loads_compressed(torque_compressed_dir, compressed_files, RE1)
except NameError:
   print 'Don\'t need compressed files'
   compressed_count = 0

# Then uncompressed 
try:
   uncompressed_count = count_loads_uncomp(torque_dir, uncomp_files, RE1)
except NameError:
   print 'Don\'t need uncompressed files'
   uncompressed_count = 0

print 'Number of module references found in specified timeframe = ' + str(compressed_count + uncompressed_count)

