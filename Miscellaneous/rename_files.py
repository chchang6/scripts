#!/usr/bin/env python3

import os, glob
import re
from sys import exit
from datetime import datetime as dt

def fs_to_dict(fs):
   # Convert file string to dictionary
   t = RE1.match(fs)
   parts_dict = {}
   parts_dict['year'] = int(t.group('year'))
   parts_dict['month'] = int(t.group('month'))
   parts_dict['day'] = int(t.group('day'))
   hour = int(t.group('hour'))
   if t.group('ampm') == 'AM':
      parts_dict['hour'] = hour
   elif t.group('ampm') == 'PM':
      parts_dict['hour'] = hour + 12
   parts_dict['minutes'] = int(t.group('minutes'))
   parts_dict['seconds'] = int(t.group('seconds'))
   return parts_dict

def fs_to_dt(fs):
   # Convert file string to datetime
   t = RE1.match(fs)
   year = int(t.group('year'))
   month = int(t.group('month'))
   day = int(t.group('day'))
   hour = int(t.group('hour'))
   minute = int(t.group('minutes'))
   second = int(t.group('seconds'))
   ampm = t.group('ampm')
   if ampm == 'PM':
      hour += 12
   return dt(year, month, day, hour, minute, second)

def sort_by_dt(fs1, fs2):
   # Take 2 file strings, return in sorted order
   t1 = fs_to_dt(fs1)
   t2 = fs_to_dt(fs2)
   if t1 < t2:
      return (t1, t2)
   elif t1 > t2:
      return (t2, t1)
   else:
      exit(f'Cannot sort files {fs1} and {fs2}')

def filter(start_dt, end_dt, file_list):
   # Inclusive to select range of files
   new_list = []
   for i in file_list:
      if not RE1.match(i): continue
      t = fs_to_dt(i)
      if (t >= start_dt) and (t <= end_dt):
         new_list.append(i)
   return(new_list)

RE1 = re.compile('Screen Shot (?P<year>20[2-9][0-9])-(?P<month>[01][0-9])-(?P<day>[0-3][0-9]) at (?P<hour>[0-9]{1,2})\.(?P<minutes>[0-9]{2})\.(?P<seconds>[0-9]{2}) (?P<ampm>[AP]M).*\.png')

allfilenames=glob.glob('Screen*')
#start_dt = dt(2020, 9, 16, 13, 34, 43)
#end_dt = dt(2021, 10, 16, 13, 46, 59)
try:
   filenames = filter(start_dt, end_dt, allfilenames)
except:
   filenames = allfilenames
for i in filenames:
   t = fs_to_dict(i)
   #print(f"{t['year']:4d}{t['month']:02d}{t['day']:02d}_{t['hour']:02d}{t['minutes']:02d}{t['seconds']:02d}" + '.png')
   os.rename(i, f"{t['year']:4d}{t['month']:02d}{t['day']:02d}_{t['hour']:02d}{t['minutes']:02d}{t['seconds']:02d}" + '.png')

