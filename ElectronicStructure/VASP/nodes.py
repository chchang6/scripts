#!/usr/bin/env python
# Script to parse nodelist, create another list for parsing out jobs from Slurm script.
#   CHC 02/14/11

import re
import os, shutil
import subprocess
import time

def breakup(x):
   y = x.split('-')
   first = int(y[0])
   last = int(y[1])
   l = []
   for i in range(first, last+1):
      l.append('rm' + str(i))
   return l

#file = open('nodelist.example', 'r')
#data = file.readlines()
#file.close()
#slurm_nodelist = data[0]
slurm_nodelist = os.getenv('SLURM_NODELIST')
nodesperjob = 4
procpernode = 8
numprocesses = nodesperjob*procpernode
homedir = os.getenv('PWD')

data = slurm_nodelist.strip()
data = data.lstrip('rm[')
data = data.rstrip(']')
data = data.split(',')
nodelist = []
for i in data:
   if not re.search('-', i): nodelist.append('rm' + i)
   else: nodelist.extend(breakup(i))
# Create scratch directories for jobs.
#TESTfor i in range(-10, 0, 5):
for i in range(-10, 55, 5):
   # Create list to hold subprocesses for polling
   jobs = []
   # Create hostlist for this job
   hostlist = ''
   for j in xrange(nodesperjob):
      host = nodelist.pop()
   #   for k in xrange(procpernode):
      hostlist += host + ','
   hostlist = hostlist.rstrip(',')
   # Create scratch directory
   scrdir = '/scratch/chchang/GgHHCrOdTNB7cu0p' + '%+1.1f' % (float(i)/10.)
   os.mkdir(scrdir)
   # Copy constant files over
   for j in ['POTCAR', 'INCAR', 'KPOINTS']:
      shutil.copy(j, scrdir)
   # Copy appropriate POSCAR file over
   shutil.copy('POSCAR' + '%+1.1f' % (float(i)/10.), scrdir + '/POSCAR')
   # Open file for stdout, change to scratch and start VASP process
   os.chdir(scrdir)
   command = 'mpirun -np ' + str(numprocesses) + ' numa_wrapper --ppn=8 `which vasp-g`'
   jobs.append(subprocess.Popen([command], shell=True))
   # Change back to Slurm working dir
   os.chdir(homedir)
# Now, cycle through processes until all are completed.
allDone = []
for i in xrange(len(jobs)):
   allDone.append(False)
while True:
   for i in xrange(len(jobs)):
      if jobs[i].poll() != None:  # Process is finished
         allDone[i] = True
   if False in allDone:  # Still at least 1 process not finished
      time.sleep(60)
   else:
      break
