#!/usr/bin/env python
# Script to convert XML version of job database to SQLite.
# Options control whether a full (stripping out undesired tags and DB creation) or
#   partial (direct, no stripping, with insertion) conversion, and
#   an update (date determination, XML processing, full conversion, and row insertion) or
#   a creation (just create new SQLite DB from XML data) is done.

import re
import gzip
import optparse
import os
#import subprocess
import sqlite3
import sys
from xml.etree import ElementTree as ET
#from shutil import copyfile
#from os.path import exists
from datetime import date

def get_string(my_element, findtext):
   #print my_element
   #print findtext
   a = my_element.find(findtext)
   if a == None:
      return ''
   else:
      return ET.tostring(a)

def get_text_ret_quotes(my_element, findtag):
   a = my_element.find(findtag)
   if a == None:
      return '" "'
   else:
      return a.text

def get_text_ret_space(my_element, findtag):
   a = my_element.find(findtag)
   if a == None:
      return ' '
   else:
      return a.text

def get_maxtime(c):
   # c is a cursor with selection of times
   t = []
   for i in c.fetchall():
      try:
         t.append(int(i[0]))
      except ValueError:
         continue
   return max(t)
   
def clean_text(stringlist):
   # Clean up bad </JobId> tags and unallowed characters in-place
   for i in xrange(len(stringlist)):
      t = stringlist[i]
      t = t.lstrip()
      t = re.sub('</JobId>', '</Job_Id>', t)
      stringlist[i] = t
      # <job_script> content is particularly troublesome, parse ahead and correct bad XML characters
      if re.search('<job_script>', t):
         j = 1
         while not re.search('</job_script>', stringlist[i+j]):
            t = re.sub('(&)(?=[^a])', '&amp;', stringlist[i+j])
            stringlist[i+j] = re.sub('<', '&lt;', stringlist[i+j])
            stringlist[i+j] = re.sub('>', '&gt;', stringlist[i+j])
            stringlist[i+j] = re.sub('"', '&quot;', stringlist[i+j])
            stringlist[i+j] = re.sub('\'', '&apos;', stringlist[i+j])
            j += 1
   return

RE1 = re.compile('<mtime>([0-9]{10})</mtime>')
RE2 = re.compile('[0-9]{8}')
RE3 = re.compile('<Jobinfo>')

parser = optparse.OptionParser()
parser.add_option('-c', '--create-from-xml', action='store_true', dest='create', default=False, help='Create SQL database from well-formed XML, strip extraneous tags')
parser.add_option('-u', '--update-from-logs', action='store_true', dest='update', default=False, help='Update existing SQL from job logs on admin2')
(options, args) = parser.parse_args()

# Check input status
if options.create: t1 = 'create'
elif options.update: t1 = 'update'
else:
   parser.print_help()
   sys.exit('Must pass either -c (create) or -u (update)')

# Get necessary input
dbname = 'test.db'
#dbname = raw_input('Name of SQLite database: ')
if options.create:
   XMLname = 'test_db.xml'
   #XMLname = raw_input('Name of input XML file: ')
else:
   XMLname = '/var/spool/torque/job_logs/'
#print 'Going to ' + t1 + ' an SQL database named ' + dbname + ' from ' + XMLname
#t = raw_input('OK (y/n)? ')
#if t != 'y':
#   sys.exit()

# Whether updating or creating, open the SQLite database and establish connection
# Doing now permits last date determination for updates.
connection = sqlite3.connect(dbname)
connection.text_factory = sqlite3.OptimizedUnicode
cursor = connection.cursor()
   
lastjob = 0
if options.create:  # Either simply converting, or updating and converting
   # Set up table
   cursor.execute('''CREATE TABLE jobs( 
    Job_Id INTEGER(7),
    Job_Name TEXT,
    Job_Owner VARCHAR(40),
    job_state CHAR(1),
    queue VARCHAR(16),
    server VARCHAR(28),
    ctime TIMESTAMP,
    etime TIMESTAMP,
    mtime TIMESTAMP,
    qtime TIMESTAMP,
    comp_time TIMESTAMP,
    start_time TIMESTAMP,
    start_count INTEGER(3),
    Error_Path VARCHAR(512),
    Output_Path VARCHAR(512),
    exec_host VARCHAR(1024),
    Rerunable NUMERIC,
    resources_reqd XML,
    resources_used XML,
    session_id SMALLINT,
    substate INTEGER(2),
    Variable_List TEXT,
    euser VARCHAR(16),
    egroup VARCHAR(16),
    queue_rank INTEGER(6),
    exit_status INTEGER(3),
    submit_args VARCHAR(512),
    submit_host VARCHAR(64),
    job_script TEXT,
    special XML)''')

   if XMLname[-2:] == 'gz':
      file = gzip.open(XMLname, 'rb')
   else:
      try:
         file = open(XMLname, 'r')
      except:
         sys.exit('Couldn\'t open file ' + XMLname)
   data = file.readlines()
   file.close()
   # Have to clean up file contents first
   clean_text(data)
   print [t for t in data if 'Finished R job' in t]
   root = ET.fromstringlist(data)
   jobs = root.iter('Jobinfo')
else: # Updating from job logs. Collect and create XML in memory
   # Get last time from existing SQLite database.
   comptimes = cursor.execute("SELECT comp_time FROM jobs")
   lasttime = get_maxtime(comptimes)
   start_date = date.fromtimestamp(lasttime)
   # What is the last jobID already in SQL database?
   t = cursor.execute("SELECT Job_Id FROM jobs")
   for i in t.fetchall():  # i of form '######.admin[1-4]'; just strip off last 7 characters
      if int(i[0]) > lastjob: lastjob = int(i[0])

   start_file = str(start_date.year) + '%02i' % start_date.month + '%02i' % start_date.day
   all_files = os.listdir(XMLname)
   uncomp_files = []
   for i in all_files:
      if not RE2.match(i): continue
      t = date(int(i[0:4]), int(i[4:6]), int(i[6:]))
      if t >= start_date:
         uncomp_files.append(i)
   
   datalist= ['<master>']
   for i in uncomp_files:
      print 'Updating from ' + i
      file = open(XMLname + i, 'r')
      data = file.readlines()
      file.close()
      clean_text(data)
   datalist.append('</master>\n') 

   # Now have full update in text XML, make in-memory XML
   root = ET.fromstringlist(datalist)
   jobs = root.iter('Jobinfo')

# Insert into table if jobid > lastjob
for i in jobs:
   jobid = int(i.find('Job_Id').text[0:-7])
   if jobid > lastjob:
      Job_Name = get_text_ret_space(i, 'Job_Name')
      Job_Owner = get_text_ret_space(i, 'Job_Owner')
      job_state = get_text_ret_space(i, 'job_state')
      queue = get_text_ret_space(i, 'queue')
      server = get_text_ret_space(i, 'server')
      ctime = get_text_ret_quotes(i, 'ctime')
      etime = get_text_ret_quotes(i, 'etime')
      mtime = get_text_ret_quotes(i, 'mtime')
      qtime = get_text_ret_quotes(i, 'qtime')
      comp_time = get_text_ret_quotes(i, 'comp_time')
      start_time = get_text_ret_quotes(i, 'start_time')
      start_count = get_text_ret_quotes(i, 'start_count')
      Error_Path = get_text_ret_space(i, 'Error_Path')
      Output_Path = get_text_ret_space(i, 'Output_Path')
      exec_host = get_text_ret_space(i, 'exec_host')
      Rerunable = get_text_ret_quotes(i, 'Rerunable')
      resources_reqd = ET.tostring(i.find('Resource_List'))
      resources_used = get_text_ret_space(i, 'resources_used')
      session_id = get_text_ret_quotes(i, 'session_id')
      substate = get_text_ret_quotes(i, 'substate')
      Variable_List = get_text_ret_space(i, 'Variable_List')
      euser = get_text_ret_space(i, 'euser')
      egroup = get_text_ret_space(i, 'egroup')
      queue_rank = get_text_ret_quotes(i, 'queue_rank')
      exit_status = get_text_ret_quotes(i, 'exit_status')
      submit_args = get_text_ret_space(i, 'submit_args')
      submit_host = get_text_ret_space(i, 'submit_host')
      job_script = get_text_ret_space(i, 'job_script')
      # Get sporadic information if present
      special = get_string(i, 'sched_hint') + \
                get_string(i, 'Shell_Path_List') + \
                get_string(i, 'forward_x11') + \
                get_string(i, 'comment') + \
                get_string(i, 'interactive') + \
                get_string(i, 'job_arguments') + \
                get_string(i, 'Mail_Users') + \
                get_string(i, 'init_work_dir') + \
                get_string(i, 'x') + \
                get_string(i, 'umask')
      # Put row in table
      SQL_command = 'INSERT INTO jobs VALUES(' + str(jobid) + ', "' + Job_Name + \
        '", "' + Job_Owner + '", "' + job_state + '", "' + queue + '", "' + server + \
        '", ' + ctime + ', ' + etime + ', ' + mtime + ', ' + qtime + \
        ', ' + comp_time + ', ' + start_time + ', ' + start_count + \
        ', "' + Error_Path + '", "' + Output_Path + '", "' + exec_host + \
        '", ' + Rerunable + ', "' + resources_reqd + '", "' + resources_used + \
        '", ' + session_id + ', ' + substate + ', "' + Variable_List + \
        '", "' + euser + '", "' + egroup + '", ' + queue_rank + ', ' + exit_status + \
        ', "' + submit_args + '", "' + submit_host + '", "' + job_script + '", "' + special + '")'
      #print SQL_command
      cursor.execute(SQL_command)

# Close DB
connection.commit()
connection.close()

# Undesired information: ['Checkpoint', 'exec_port', 'Hold_Types', 'Join_Path', 'Keep_Files', 'Mail_Points', 'Priority',
#            'hashname', 'hop_count', 'queue_type', 'fault_tolerant', 'job_radix', 'total_runtime', \
#            'node_exclusive', 'queue_type']

