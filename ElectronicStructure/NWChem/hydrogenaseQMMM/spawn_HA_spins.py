#!/usr/bin/env python
# Script to autogenerate NWChem input files for all 6 inversion-unique spin
#   arrangements among [4Fe4S] center on HYDHA. CHC 12/2/09.
#   12/30/09: Modify to enable o/r valences of [4Fe4S]

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

pbsdata=['#!/bin/ksh -l\n', '#PBS -l mppwidth=64\n', '#PBS -l walltime=02:30:00\n', '#PBS -N B_\n', '#PBS -A m514\n', '#PBS -j oe\n', '#PBS -q regular\n', '#PBS -m abe\n', '#PBS -M user.name@domain.name\n', '#PBS -V\n', '\n', 'JOBFILE=\n', 'AUXFILES=""\n', 'LOGFILE=$PBS_O_WORKDIR/\n', 'SCRDIR=\n' ,'SCRAPFILES="*[23]ceri* *.grinfo.* *.gridpts.* *.b *.b^-1 *.c *.cdfit"\n' ,'\n' ,'module load nwchem\n' ,'\n', 'if [ -d $SCRDIR ]\n', 'then\n', 'rm -rf $SCRDIR\n', 'fi\n', 'mkdir $SCRDIR\n', 'cd $SCRDIR\n', 'cp $PBS_O_WORKDIR/$JOBFILE .\n', 'for x in $AUXFILES; do cp $PBS_O_WORKDIR/$x .; done\n', 'chmod 600 *\n', '\n', 'aprun -n 64 `which nwchem` $JOBFILE > $LOGFILE\n', '\n', 'echo "Files in scratch"\n', 'ls -l\n', 'rm $SCRAPFILES\n', 'tar -czf keep2.tgz *\n', 'cp keep2.tgz $PBS_O_WORKDIR\n']

import re, os, shutil, copy, sys
import optparse

parser = optparse.OptionParser()
parser.add_option('-v', '--valence', action='store', type='string', dest='valence', help='[4Fe4S] HYDA cluster valence (o = 2+, r = 1+)')
(options, args) = parser.parse_args()

RE1 = re.compile(r'41a1_422_([0-9]+a[23]_){3}[0-9]+a[23]\.nw')

if not RE1.match(args[0]):
   raise IOError('Input filename is expected to be form AaV_AV_AaV_AaV_AaV_AaV.nw, with A = Arabic number of atomic index, a = literal "a", and V = arabic valence.')
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

# Create list of lists with all inversion-unique spin orderings for 4 centers.
# Examine valence pattern of input filename. Determine feasible patterns therefrom.
# For now, assume HYDH left out; just look at last 4 valences. This changes
valences = args[0][0:-3].split('_')
arabic_valences = []
for i in valences[2:]:
   arabic_valences.append(i[-1])
x = []
if options.valence == 'o':
   # Oxidized cluster.
   # Assign first spin as majority-alpha. Then one of the two other valence types must be
   #   majority-alpha as well. The other two are beta.
   charge = '-3'
   for i in ['a', 'b']:
      x.append([i, 'n', 'n', 'n'])
      for j in range(1,4):
         if arabic_valences[j] == arabic_valences[0]:
            same_valence = j
            break
      if i == 'a': x[-1][same_valence] = 'b'
      else: x[-1][same_valence] = 'a'
      temp = True
      for j in range(1,4):
         if x[-1][j] == 'n' and temp == True:
            x[-1][j] = 'a'
            temp = False
         elif x[-1][j] == 'n' and temp == False:
            x[-1][j] = 'b'
      other_spin_list = [i]
      for j in range(1,4): 
         if j == same_valence and i == 'a':
            other_spin_list.append('b')
         elif j == same_valence and i == 'b':
            other_spin_list.append('a')
         elif j != same_valence and x[-1][j] == 'a':
            other_spin_list.append('b')
         else:
            other_spin_list.append('a')
      x.append(other_spin_list)     
elif options.valence == 'r':
   # Reduced cluster.
   # Assign ferric ion as either majority-alpha or -beta. For illustration, if ferric = 'a', ferrous ions will
   #  be in {['b','b','a'], ['b','a','b'], ['a','b','b']}. Vice-versa for ferric = 'b' --> six possible combinations.
   charge = '-4'
   ferric_index = arabic_valences.index('3')
   ferric_a_set = [['b','b','a'], ['b','a','b'], ['a','b','b']]
   ferric_b_set = [['a','a','b'], ['a','b','a'], ['b','a','a']]
   temp = ['n','n','n','n']
   temp[ferric_index] = 'a'
   for i in ferric_a_set:
      j = 0
      while j < 4:
         if j != ferric_index:
            temp[j] = i.pop(0)
         j += 1
      x.append(copy.deepcopy(temp))
   temp[ferric_index] = 'b'
   for i in ferric_b_set:
      j = 0
      while j < 4:
         if j != ferric_index:
            temp[j] = i.pop(0)
         j += 1
      x.append(copy.deepcopy(temp))
else:
   sys.exit('Must specify cubane valence with -v option. Type ' + sys.argv[0] + ' -h for syntax.')

print x

head = ['memory total 1600 mb global 1000 mb\n', \
'ECHO\n', refdata[3], 'print medium\n', \
'\n', 'basis "ao basis" spherical\n', '  Fe library 6-31g*\n', '   S library 6-31+g*\n', \
'   O library 6-31+g*\n', '   N library 6-31+g*\n', '   C library 6-31g*\n', '   H library 6-31g**\n', \
'end\n', '\n', 'basis "cd basis" spherical\n', '   * library "Ahlrichs Coulomb Fitting"\n', 'end\n', '\n']
 
# Replace Bq lines with Fe names in turn. Fe_dict[0] and [1] refer to H-cluster ions, so skip.
for i in x:
   tail = ['\n', 'charge ' + charge, '\n', 'set geometry cluster\n', 'dft\n', \
   'odft; mult 2\n']
   Fe1 = Fe_dict[2] + i[0]
   Fe2 = Fe_dict[3] + i[1]
   Fe3 = Fe_dict[4] + i[2]
   Fe4 = Fe_dict[5] + i[3]
   vecinput_string = 'vectors fragment Fe41a.movecs Fe42.movecs ' # Base vectors, assuming H-cluster assigned spin alpha with atoms 41 and 42.
   MOvectors_list = [Fe1 + '.movecs ', Fe2 + '.movecs ', Fe3 + '.movecs ', Fe4 + '.movecs ']
   for j in MOvectors_list:
      vecinput_string += j
   vecinput_string += 'ligs.movecs output cluster.movecs\n'
   tail.append(vecinput_string)
   tail.extend(['   iterations 400\n', '   convergence damp 70 ncydp 40 lshift\n', \
   'end\n', 'task dft energy\n'])
   Fe_names = ['Fe41', 'Fe42', Fe1, Fe2, Fe3, Fe4]
   counter = 0
   geom_copy = copy.deepcopy(geom)
   for j in xrange(len(geom_copy)):
      if geom_copy[j][0:2] == 'Bq':
         geom_copy[j] = re.sub('Bq', Fe_names[counter], geom_copy[j])
         geom_copy[j] = re.sub(' charge .*$', '', geom_copy[j])
         counter += 1

   # Now open new file and write
   file_string = '41a1_422_' + \
                 re.sub('Fe','',Fe1) + arabic_valences[0] + '_' + \
                 re.sub('Fe','',Fe2) + arabic_valences[1] + '_' + \
                 re.sub('Fe','',Fe3) + arabic_valences[2] + '_' + \
                 re.sub('Fe','',Fe4) + arabic_valences[3] + '.nw'

   # Change start line in data. Assumed to be in form AaV_AV_AaV_AaV_AaV_AaV (second entry reflects low-spin ferrous)
   start_string = refdata[0].rstrip().split()[1]
   temp = re.split('_', start_string)
   start_string = 'start ' + file_string[0:-3] + '\n'
   # Start writing
   os.mkdir(file_string[0:-3])
   shutil.copy('Fe41a.movecs',file_string[0:-3])
   shutil.copy('Fe42.movecs',file_string[0:-3])
   for j in MOvectors_list:
      shutil.copy(j.rstrip(),file_string[0:-3])
   shutil.copy('ligs.movecs', file_string[0:-3])
   os.chdir(file_string[0:-3])
   pbs_new_file = open(start_string[5:].strip() + '.pbs', 'w')
   j = 0
   while j < len(pbsdata):
      if re.search('#PBS -N', pbsdata[j]):
         k = '#PBS -N HA_' + start_string[5:].strip() + '\n'
      elif re.search('^JOBFILE', pbsdata[j]):
         k = 'JOBFILE=' + file_string + '\n'
      elif re.search('^LOGFILE', pbsdata[j]):
         k = 'LOGFILE=$PBS_O_WORKDIR/DFT2.log\n'
      elif re.match('^AUXFILES=""', pbsdata[j]):
         k = 'AUXFILES="*.movecs"\n'
      elif re.search('SCRDIR=', pbsdata[j]):
         if options.valence == 'o':
            k = 'SCRDIR=$SCRATCH/HAox_sp/' + file_string[0:-3] + '\n'
         else:
            k = 'SCRDIR=$SCRATCH/HAred_sp/' + file_string[0:-3] + '\n'
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
   for j in geom_copy:
      outfile.write(j)
   outfile.write('end\n')
   for j in tail:
      outfile.write(j)
   outfile.close()
   os.chdir('..')
