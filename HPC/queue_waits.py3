#!/usr/bin/env python
# Script to get job wait times from squeue output

import re
import subprocess
import datetime
from collections import namedtuple

RE_running_time = re.compile('(?P<days>[0-9]{1,2})?-?(?P<hours>[0-9]{1,2})?:?(?P<minutes>[0-9]{1,2}):(?P<seconds>[0-9]{2})')
job = namedtuple('Job', ['index', 'priority', 'running_time', 'status', 'start', 'submit', 'wait'])

def run_time(rt_string):
   try:
      t = RE_running_time.match(rt_string)
   except AttributeError:
      print(rt_string)
      return
   days = int(t.group('days')) if t.group('days') else 0
   hours = int(t.group('hours')) if t.group('hours') else 0
   minutes = int(t.group('minutes'))
   seconds = int(t.group('seconds'))
   return datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

def seconds_to_pretty(td):
   # Convert timedelta in seconds
   seconds = td % 60
   td_minutes = td // 60
   minutes = td_minutes % 60
   td_hours = td_minutes // 60
   hours = td_hours % 24
   td_days = td_hours // 24
   return '{:2d} days, {:02d}:{:02d}:{:02d}'.format(td_days, hours, minutes, seconds)

base_query = 'squeue -o %.8i%.10Q%.12M%.10T%.25S%.25V'
data = subprocess.getoutput(base_query).split('\n')[1:]
job_list = []
for i in data:
   t = i.split()
   t2 = RE_running_time.match(t[2])
   if t[3] == 'PENDING':
      wait_time = datetime.datetime.now() - datetime.datetime.fromisoformat(t[5])
   else:
      #print(t)
      wait_time = datetime.datetime.fromisoformat(t[4]) - datetime.datetime.fromisoformat(t[5])
   job_list.append( job(index = t[0],
                    priority = int(t[1]),
                    running_time = run_time(t[2]),
                    status = t[3],
                    start = -1 if t[4] == 'N/A' else datetime.datetime.fromisoformat(t[4]),
                    submit = datetime.datetime.fromisoformat(t[5]),
                    wait = wait_time))

job_list.sort(key = lambda x: x.wait)
for i in job_list:
   print('Job {} with priority {} has status {} and waited {}'.format(i.index, i.priority, i.status, seconds_to_pretty(int(i.wait.total_seconds()))))

