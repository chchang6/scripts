#!/usr/bin/env python

import re
import glob

RE1 = re.compile('<queue>')
RE2a = re.compile('<euser>')
RE2b = re.compile('</euser>\n')
RE3 = re.compile('short')
RE4a = re.compile('<qtime>')
RE4b = re.compile('</qtime>\n')
RE5a = re.compile('<start_time>')
RE5b = re.compile('</start_time>\n')
RE6 = re.compile('<interactive>')

users = {}

files = glob.glob('/var/spool/torque/job_logs/2014*')
for i in files:
   file = open(i)
   data = file.readlines()
   file.close()
   for i in xrange(len(data)):
      if RE1.search(data[i]) and RE3.search(data[i]):
         wait_time = 0
         interactive = False
         for j in xrange(100):
            try:
               if RE2a.search(data[i+j]):
                  this_user = re.sub(RE2a, '', data[i+j])
                  this_user = re.sub(RE2b, '', this_user)
                  this_user = this_user.lstrip('\t')
                  if this_user in users: users[this_user][0] += 1
                  else: users[this_user] = [1,0,0]  # [job count, # more than 1 minute]
               elif RE6.search(data[i+j]): interactive = True
               elif RE4a.search(data[i+j]):
                  t = re.sub(RE4a, '', data[i+j])
                  t = re.sub(RE4b, '', t)
                  wait_time = int(t)
               elif RE5a.search(data[i+j]):
                  t = re.sub(RE5a, '', data[i+j])
                  t = re.sub(RE5b, '', t)
                  wait_time = int(t) - wait_time
                  if wait_time > 3600:
                     users[this_user][1] += 1
                     if interactive: users[this_user][2] += 1
                  break
            except IndexError: break

print 'User: [short or shortphi jobs, number > 3600s wait, number interactive > 3600 s wait]'
# Change 2nd lambda index to sort on short, >3600 wait, or >3600 interactive wait
sorted_by_value = sorted(users.iteritems(), key=lambda x: x[1][0], reverse=True)
for i in sorted_by_value:
   print i[0] + ': ' + str(i[1])

