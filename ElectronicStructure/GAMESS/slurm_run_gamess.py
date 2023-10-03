#!/usr/bin/env python
# Script to generate Slurm input file for GAMESS run.
#   CHC 02/12/10

def wrong_options(option):
   if option == 'time':
      print_string='You have not specified the time properly!'
   elif option == 'numnodes':
      print_string='You have not specified the number of nodes you want!'
   elif option == 'numprocesses':
      print_string='You have not specified the number of processes you want!'
   print print_string
   option_parser.print_help()
   sys.exit()
   
slurmdata=['#!/bin/bash -l\n', '#SBATCH --time=', '#SBATCH -N ', '#SBATCH -n ', '#SBATCH --job-name ', '#SBATCH -p ', '#SBATCH --ntasks-per-node ', 'export SLURM_WORKING_DIR=`pwd`\n', 'export SCRATCH=$HOME/scratch/', 'INPUT_FILE=', '# Note that your scratch files will be in $HOME/scratch/job-name\n', '# The following is a default workflow. Modify according to your specific needs\n\n', 'if [ -d $SCRATCH ]\n', 'then\n', '   cd $SCRATCH\n', 'else\n', '   mkdir $SCRATCH\n', '   cd $SCRATCH\n', 'fi\n', 'cp $SLURM_WORKING_DIR/* .', '# Modify the following line to redirect output and error to the appropriate file is desired\n', 'rungms ']

import re, sys, os, shutil
from optparse import OptionParser

GAMESS_version = '00'
RE1 = re.compile('#SBATCH --time=')
RE2 = re.compile('#SBATCH -N ')
RE3 = re.compile('#SBATCH -n ')
RE4 = re.compile('#SBATCH --job-name ')
RE5 = re.compile('#SBATCH -p ')
RE6 = re.compile('#SBATCH --ntasks-per-node')
RE7 = re.compile('export SCRATCH')
RE8 = re.compile('rungms')
RE9 = re.compile('INPUT_FILE')

usage = 'Usage: nrel_run_gamess [options] file.inp'
option_parser = OptionParser(usage=usage)
option_parser.add_option('-t', '--time', help='Total wallclock time request', dest='t')
option_parser.add_option('-N', help='Number of nodes requested', dest='N')
option_parser.add_option('-n', help='Total number of processes requested', dest='n')
option_parser.add_option('--job-name', default=sys.argv[-1][:-4], help='Name of your job. By default, this will be the input file basename', dest='jobname')
option_parser.add_option('-p', default='pbatch', help='Batch queue requested. Default is pbatch', dest='p')
option_parser.add_option('--TPN', default='8', help='Tasks per node requested. Default value = 8 for Red Rock.', dest='TPN')
(options, args) = option_parser.parse_args()
for i in xrange(len(slurmdata)):
   if RE1.match(slurmdata[i]):
      if option_parser.has_option('-t'):
         slurmdata[i] += options.t + '\n'
      else:
         wrong_options('time')
   elif RE2.match(slurmdata[i]):
      if option_parser.has_option('-N'):
         slurmdata[i] += options.N + '\n'
      else:
         wrong_options('numnodes')
   elif RE3.match(slurmdata[i]):
      if option_parser.has_option('-n'):
         slurmdata[i] += options.n + '\n'
      else:
         wrong_options('numprocesses')
   elif RE4.match(slurmdata[i]):
      slurmdata[i] += options.jobname + '\n'
   elif RE5.match(slurmdata[i]):
      slurmdata[i] += options.p + '\n'
   elif RE6.match(slurmdata[i]):
      slurmdata[i] += options.TPN + '\n\n'
   elif RE7.match(slurmdata[i]):
      slurmdata[i] += options.jobname + '\n'
   elif RE8.match(slurmdata[i]):
      slurmdata[i] += args[0] + ' ' + GAMESS_version + ' ' + options.n + '\n'
   elif RE9.match(slurmdata[i]):
      slurmdata[i] += args[0] + '\n'
   else: continue

   # Start writing
try:
   os.mkdir(options.jobname)
   shutil.copy(args[0], options.jobname)
   os.chdir(options.jobname)
   slurm_new_file = open(args[0][:-4] + '.slurm', 'w')
   for i in slurmdata:
      slurm_new_file.write(i)
   slurm_new_file.close()
except OSError:
   sys.exit('Directory ' + options.jobname + ' already exists!')
#else:
#   sys.exit('Unknown error')
