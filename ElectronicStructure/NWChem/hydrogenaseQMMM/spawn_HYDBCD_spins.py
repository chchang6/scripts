#!/usr/bin/env python
# Script to autogenerate NWChem input files for all 3 inversion-unique spin
#   arrangements among oxidized [4Fe4S]2+ centers. CHC 10/26/09.

def proc(line):
   global refdata
   j = line + 1
   flag = True
   list = []
   while flag:
      if refdata[j] == 'end\n': flag = False
      else:
         list.append(refdata[j])
         j += 1
   return list

pbsdata=['#!/bin/ksh -l\n', '#PBS -l mppwidth=64\n', '#PBS -l walltime=03:00:00\n', '#PBS -N Bred_\n', '#PBS -A m514\n', '#PBS -j oe\n', '#PBS -q regular\n', '#PBS -m abe\n', '#PBS -M user.name@domain.name\n', '#PBS -V\n', '\n', 'JOBFILE=\n', 'AUXFILES="*.movecs"\n', 'LOGFILE=$PBS_O_WORKDIR/DFT2.log\n', 'SCRDIR=\n' ,'SCRAPFILES="*[23]ceri* *.grinfo.* *.gridpts.* *.b *.b^-1 *.c *.cdfit"\n' ,'\n' ,'module load nwchem\n' ,'\n', 'if [ -d $SCRDIR ]\n', 'then\n', 'rm -rf $SCRDIR\n', 'fi\n', 'mkdir $SCRDIR\n', 'cd $SCRDIR\n', 'cp $PBS_O_WORKDIR/$JOBFILE .\n', 'for x in $AUXFILES; do cp $PBS_O_WORKDIR/$x .; done\n', 'chmod 600 *\n', '\n', 'aprun -n 64 `which nwchem` $JOBFILE > $LOGFILE\n', '\n', 'echo "Files in scratch"\n', 'ls -l\n', 'rm $SCRAPFILES\n', 'tar -czf keep2.tgz *\n', 'cp keep2.tgz $PBS_O_WORKDIR\n']

import re, sys, os, shutil
import optparse, copy
option_parser = optparse.OptionParser()
option_parser.add_option('-v', '--valence', action='store', type='string', dest='valence', help='Cluster valence (o = 2+, r = 1+)')
(options, args) = option_parser.parse_args()

RE1 = re.compile(r'([0-9]+a[23]_){3}[0-9]+a[23]\.nw')

if not RE1.match(args[0]):
   raise IOError('Input filename is expected to be form AaV_AaV_AaV_AaV.nw, with A = Arabic number of atomic index, a = literal "a", and V = arabic valence.')
else:
   file = open(args[0], 'r')
   refdata = file.readlines()
   file.close()

FeCounter = 0
Fe_dict = {}
for i in xrange(len(refdata)):
   geomflag = ''
   multflag = ''
   if refdata[i][0:11] == 'geometry Fe':
      Fe_dict[FeCounter] = refdata[i].split()[1]
      FeCounter += 1
   if refdata[i][0:16] == 'geometry ligands':
      geom = proc(i)

# Oxidized cluster--assumes '-o' flag passed to script.
# Create list of lists with all inversion-unique spin orderings for 4 centers.
# Examine valence pattern of input filename. Determine feasible patterns therefrom.
valences = args[0][0:-3].split('_')
arabic_valences = []
for i in valences:
   arabic_valences.append(i[-1])
if options.valence == 'o':
   # Assign first spin as majority-alpha. Then one of the two other valence types must be
   #   majority-alpha as well. The other two are beta.
   x = [['a','n','n','n']]
   for i in range(1,4):
      if arabic_valences[i] == arabic_valences[0]:
         same_valence = i
         break
   x[0][i] = 'b'
   temp = True
   for i in range(1,4):
      if x[0][i] == 'n' and temp == True:
         x[0][i] = 'a'
         temp = False
      elif x[0][i] == 'n' and temp == False:
         x[0][i] = 'b'
   other_spin_list = ['a']
   for i in range(1,4): 
      if i == same_valence:
         other_spin_list.append('b')
      elif i != same_valence and x[0][i] == 'a':
         other_spin_list.append('b')
      else:
         other_spin_list.append('a')
   x.append(other_spin_list)     
elif options.valence == 'r':
   # Assign ferric ion majority-alpha. Then create all combinations of a and 2b over other ions
   x = [['n', 'n', 'n', 'n']]
   for i in xrange(4):
      if arabic_valences[i] == '3':
         x[0][i] = 'a'
         break
   combos = [('a','b','b'), ('b', 'a', 'b'), ('b', 'b', 'a')]
   x.append(copy.deepcopy(x[0]))
   x.append(copy.deepcopy(x[0]))
   for i in xrange(len(x)):
      combo_index = 0
      for j in xrange(len(x[i])):
         if x[i][j] == 'n':
            x[i][j] = combos[i][combo_index]
            combo_index += 1
else: sys.exit('Valence option must be set. Use ' + sys.argv[0] + ' -h')

print x

head = ['memory total 1600 mb global 1000 mb\n', \
'ECHO\n', refdata[3], 'print medium\n', \
'\n', 'basis "ao basis" spherical\n', '  Fe library 6-31g*\n', '   S library 6-31+g*\n', \
'   O library 6-31+g*\n', '   N library 6-31+g*\n', '   C library 6-31g*\n', '   H library 6-31g**\n', \
'end\n', '\n', 'basis "cd basis" spherical\n', '   * library "Ahlrichs Coulomb Fitting"\n', 'end\n', '\n']
 
# Replace Bq lines with Fe names in turn
for i in x:
   Fe1 = Fe_dict[0] + i[0]
   Fe2 = Fe_dict[1] + i[1]
   Fe3 = Fe_dict[2] + i[2]
   Fe4 = Fe_dict[3] + i[3]
   MOvectors_list = [Fe1 + '.movecs ', Fe2 + '.movecs ', Fe3 + '.movecs ', Fe4 + '.movecs ']
   tail = ['\n', 'charge -3.0', '\n', 'set geometry cluster\n', 'dft\n', \
   'odft; mult 2\n']
   vecinput_string = 'vectors fragment '
   for j in MOvectors_list:
      vecinput_string += j
   vecinput_string += 'ligs.movecs output cluster.movecs\n'
   tail.append(vecinput_string)
   tail.extend(['   iterations 1000\n', '   convergence damp 70 ncydp 40 lshift\n', \
   'end\n', 'task dft energy\n'])
   Fe_names = [Fe1, Fe2, Fe3, Fe4]
   counter = 0
   for j in xrange(len(geom)):
      if geom[j][0:2] == 'Bq':
         geom[j] = re.sub('Bq', Fe_names[counter], geom[j])
         geom[j] = re.sub(' charge .*$', '', geom[j])
         counter += 1

   # Now open new file and write
   file_string = re.sub('Fe','',Fe1) + arabic_valences[0] + '_' + \
                 re.sub('Fe','',Fe2) + arabic_valences[1] + '_' + \
                 re.sub('Fe','',Fe3) + arabic_valences[2] + '_' + \
                 re.sub('Fe','',Fe4) + arabic_valences[3] + '.nw'

   # Change start line in data. Assumed to be in form AAA_AAA_AAA_AAA
   start_string = refdata[0].rstrip().split()[1]
   temp = re.split('_', start_string)
   start_string = 'start ' + file_string[0:-3] + '\n'
   # Start writing
   os.mkdir(file_string[0:-3])
   for j in MOvectors_list:
      shutil.copy(j.rstrip(),file_string[0:-3])
   shutil.copy('ligs.movecs', file_string[0:-3])
   os.chdir(file_string[0:-3])
   pbs_new_file = open(start_string[5:].strip() + '.pbs', 'w')
   j = 0
   while j < len(pbsdata):
      if re.search('#PBS -N', pbsdata[j]):
         k = '#PBS -N Bred_' + start_string[5:].strip() + '\n'
      elif re.search('^JOBFILE', pbsdata[j]):
         k = 'JOBFILE=' + file_string + '\n'
      elif re.search('SCRDIR=', pbsdata[j]):
         k = 'SCRDIR=$SCRATCH/Bred_sp/' + file_string[0:-3] + '\n'
      else:
         k = pbsdata[j]
      pbs_new_file.write(k)
      j += 1
   pbs_new_file.close()
   outfile = open(file_string, 'w')
   outfile.write(start_string)
   for j in head:
      outfile.write(j)
   outfile.write('geometry cluster noautoz nocenter\n')
   for j in geom:
      outfile.write(j)
   outfile.write('end\n')
   for j in tail:
      outfile.write(j)
   outfile.close()
   os.chdir('..')
