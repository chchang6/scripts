#!/usr/bin/env python
#  Script to replace parallel header information with new Gaussian09 syntax.
#  Command syntax is linda_[system name].py Default.Route jobname.gjf
#  The node list is from "scontrol show hostname"

import os, sys, re
from subprocess import check_output, Popen, PIPE

RE1 = re.compile('%NProcLinda=(?P<numlinda>\d+)', re.I)
RE2 = re.compile('%NProcShared=(?P<numshared>\d+)', re.I)
RE3 = re.compile('%RWF=.*/dev/shm/,(?P<devshm>[0-9]*[MG])', re.I)

nodelist = check_output(['scontrol', 'show', 'hostname']).strip().split('\n')
numnodes = int(os.environ['SLURM_JOB_NUM_NODES'])
assert numnodes == len(nodelist)
mem_filesystem_mb = 0
#print('mem_filesystem_mb = %d' % mem_filesystem_mb)
# Assume that the number of Linda processes desired is specified with the following priority:
# 1. NProcLinda (note, Gaussian is deprecating this mechanism in favor of specific node naming in E.1,
#    via LindaWorkers, which will require explicit re-working of the input file anyway)
# 2. If a numerical argument is given after the jobfile, assume that this is the number of Linda workers per node.
# 3. Otherwise, assume 1 per node.
G16_job_file = open(sys.argv[1], 'r')
G16_job = G16_job_file.readlines()
G16_job_file.close()
for i in G16_job:
   if RE1.search(i):
      num_Linda_total = int(RE1.search(i).group('numlinda'))
   elif RE2.search(i):
      num_procs_shared = int(RE2.search(i).group('numshared'))
   elif RE3.search(i):
      #print('RE3 found')
      t = RE3.search(i).group('devshm')
      #print('RE3 t = %s' % t)
      t2 = int(t[0:-1])
      if t[-1] == 'G' or t[-1] == 'g':
         t2 *= 1024
      #print('RE3 t2 = %d' % t2)
      mem_filesystem_mb = max(mem_filesystem_mb, t2)
      #print('RE3 mem_filesystem_mb = %d' % mem_filesystem_mb)
   else:
      try:
         if num_Linda_total and num_procs_shared:
            break
      except NameError:
         continue

# Figure out how many Linda workers per node.
try:
   num_Linda_total
except NameError:
   # Since there was apparently no NProcLinda directive in the input file, see if it was on command line
   try:
      num_Linda_total = int(sys.argv[2]) * numnodes
   except IndexError:
      num_Linda_total = numnodes

Linda_workers_per_node = num_Linda_total // numnodes

# Find out core count of nodes we have been assigned.
cores_per_node = int(check_output(['grep', '-c', 'processor', '/proc/cpuinfo']))
# Right now, if there are more than 36 apparent cores per node, we have hit a node with
#   hyperthreading. Divide apparent core count by 2.
if cores_per_node > 36:
   cores_per_node /= 2
# Test only
#cores_per_node = 36

# Assume threading multiplicity is specified with the following priority:
# 1. NProcShared in input, but check that there aren't too many for the number of Linda workers
# 2. If no NProcShared is not specified, assume cores_per_node divided by the number of Linda workers per node
try:
   num_threads_per_worker = num_procs_shared
   if Linda_workers_per_node * num_threads_per_worker > cores_per_node:
      num_threads_per_worker /= Linda_workers_per_node
except NameError:
   num_threads_per_worker = cores_per_node // Linda_workers_per_node

# Find out how much memory is on nodes. Subtract 7 GB off limit,
#   as Gaussian seems like it may try to allocate it all at once
#   (and fails because of the OS overhead, /dev/shm set to 5GB, etc.)
t1 = Popen(['free', '-m'], stdout=PIPE)
t2 = Popen(['head', '-2'], stdin=t1.stdout, stdout=PIPE)
t1.stdout.close()
t3 = Popen(['tail', '-1'], stdin=t2.stdout, stdout=PIPE)
t2.stdout.close()
t4 = t3.communicate()[0].strip()
# 256 GB nodes sometimes create galloc errors. If mem_mb larger than threshold, fix to lower value.
mem_mb = min(int(t4.split()[3]), 96000)
# Correct for any intended use of in-memory /dev/shm filesystem, or a 7 GB buffer, whichever is larger
if mem_filesystem_mb > 7000:
   mem_mb -= mem_filesystem_mb
else:
   mem_mb -= 7000

# Turn nodelist into comma-separated string of node names.
nodestring = ''
for i in nodelist:
   nodestring += i.strip()
   if Linda_workers_per_node > 1:
      nodestring += ':' + str(Linda_workers_per_node) + ','
   else:
      nodestring += ','
# Delete trailing comma
nodestring = nodestring[0:-1]
                
# Modify custom Default.Route file
file = open('Default.Route','r')
route = file.readlines()
file.close()
# Assume that there is no previous node list in Default.Route here.
route.insert(0, '-W- ' + nodestring + '\n')
# Update -P-, -M- cards with current info
for i in range(len(route)):
   if route[i][:3] == '-P-':
      route[i] = re.sub('-P- .*', '-P- ' + str(num_threads_per_worker), route[i])
   elif route[i][:3] == '-M-':
      route[i] = re.sub('-M- .*', '-M- ' + str(mem_mb) + 'MB', route[i])
                   
out = open('Default.Route', 'w')
for i in route:
   out.write(i)
out.close()

