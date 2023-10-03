#!/usr/bin/env python
# Python script to create NWChem QMMM input deck. CHC

def wrong_options(option):
   if option == 'time':
      print_string='You have not specified the time properly!'
   elif option == 'numnodes':
      print_string='You have not specified the number of nodes you want!'
   elif option == 'numprocesses':
      print_string='You have not specified the number of processes you want!'
   elif option == 'file':
      print_string='File ' + args[0] + ' isn\'t readable!'
   print print_string
   option_parser.print_help()
   sys.exit()

import re, sys, os, shutil
import os.path
import random
import argparse

RE1 = re.compile('start')
RE2 = re.compile('title')
RE3 = re.compile('   system')
RE4 = re.compile(r'\.db')

if len(sys.argv) == 1:  # No options given
   sys.exit('Please try "make_nwc_qmmmdeck.py -h"')

datalist = ['start ','ECHO','title ', 'print medium', '', 'md', \
'   system ','end','','basis','   * library "Ahlrichs_pVDZ"','end','', \
'qmmm','   eref 0.0','   bqzone 9.0','   bqexclude linkbond','   bq_update static', \
'   link_atoms hydrogen','   link_ecp auto','   optimization qm','end', \
'','task qmmm dft energy','']

for i in os.listdir(os.getcwd()):
   if RE4.search(i):
      dbbase = i[0:-3]
   else: dbfile = None

usage = 'Usage: make_nwc_qmmmdeck.py [options] output_file_basename'
parser = argparse.ArgumentParser(description = 'Script to create NWChem QMMM single-point input file', usage=usage)
parser.add_argument('-t', '--title', default='NWChem job ' + str(random.randint(1,1e9)), help='Title string. Enclose in single quotes.', dest='t')
parser.add_argument('-s', '--start', default=dbbase, help='Name of system, default value = database basename', dest='s')
parser.add_argument('-j', '--job-name', default=dbbase, help='Name of your job. By default, database basename', dest='jobname')
parser.add_argument('filename', help='Basename of the output.nw file to be created', metavar='output_file_name')

args = parser.parse_args()
outfile = open(args.filename + '.nw', 'w')

for i in datalist:
   if RE1.match(i): i += args.s
   elif RE2.match(i): i += args.t
   elif RE3.match(i): i += args.jobname
   outfile.write(i + '\n')
outfile.close()
