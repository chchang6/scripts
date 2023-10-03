#!/usr/bin/env python
# Script to autogenerate NWChem input files for all 6 charge arrangements among
#   oxidized [4Fe4S]2+ center of H-cluster. Output will then be used to generate 2 possible
#   spin arrangements for each. CHC 11/24/09.

class atom_list:
   def __init__(self, listname, start_index, stop_index):
      self.list = listname
      self.start = start_index
      self.end = stop_index

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
   return atom_list(list, line+1, j)

pbsdata=['#!/bin/ksh -l\n', '#PBS -l mppwidth=64\n', '#PBS -l walltime=04:00:00\n', '#PBS -N B_\n', '#PBS -A m514\n', '#PBS -j oe\n', '#PBS -q regular\n', '#PBS -m abe\n', '#PBS -M user.name@domain.name\n', '#PBS -V\n', '\n', 'JOBFILE=\n', 'AUXFILES=""\n', 'LOGFILE=$PBS_O_WORKDIR/DFT1.log\n', 'SCRDIR=\n' ,'SCRAPFILES="*[23]ceri* *.grinfo.* *.gridpts.* *.b *.b^-1 *.c *.cdfit"\n' ,'\n' ,'module load nwchem\n' ,'\n', 'if [ -d $SCRDIR ]\n', 'then\n', 'rm -rf $SCRDIR\n', 'fi\n', 'mkdir $SCRDIR\n', 'cd $SCRDIR\n', 'cp $PBS_O_WORKDIR/$JOBFILE .\n', 'for x in $AUXFILES; do cp $PBS_O_WORKDIR/$x .; done\n', 'chmod 600 *\n', '\n', 'aprun -n 64 `which nwchem` $JOBFILE > $LOGFILE\n', '\n', 'echo "Files in scratch"\n', 'ls -l\n', 'rm $SCRAPFILES\n', 'tar -czf keep1.tgz *\n', 'cp keep1.tgz $PBS_O_WORKDIR\n']

import re, sys, os, shutil
import optparse

parser = optparse.OptionParser()
parser.add_option('-v', '--valence', action='store', type='string', dest='valence', help='[4Fe4S] HYDA cluster valence (o = 2+, r = 1+)')
(options, args) = parser.parse_args()

RE1 = re.compile('MULT')
file = open('template.nw', 'r')
refdata = file.readlines()
file.close()

for i in xrange(len(refdata)):
   geomflag = ''
   multflag = ''
   if refdata[i][0:13] == 'geometry Fe63': geomflag = 'first_iron'
   elif refdata[i][0:13] == 'geometry Fe64': geomflag = 'second_iron'
   elif refdata[i][0:13] == 'geometry Fe65': geomflag = 'third_iron'
   elif refdata[i][0:13] == 'geometry Fe66': geomflag = 'fourth_iron'
   elif refdata[i][0:16] == 'geometry ligands': geomflag = 'ligands'
   elif refdata[i] == 'set geometry Fe63\n': multflag = 'first_iron'
   elif refdata[i] == 'set geometry Fe64\n': multflag = 'second_iron'
   elif refdata[i] == 'set geometry Fe65\n': multflag = 'third_iron'
   elif refdata[i] == 'set geometry Fe66\n': multflag = 'fourth_iron'
   elif refdata[i] == 'set geometry full\n': multflag = 'full'
   flag = True
   if geomflag == 'first_iron':
      iron1_list = proc(i)
   if geomflag == 'second_iron':
      iron2_list = proc(i)
   if geomflag == 'third_iron':
      iron3_list = proc(i)
   if geomflag == 'fourth_iron':
      iron4_list = proc(i)
   if geomflag == 'ligands':
      lig_list = proc(i)
   if multflag == 'first_iron':
      iron1_dft = proc(i)
   if multflag == 'second_iron':
      iron2_dft = proc(i)
   if multflag == 'third_iron':
      iron3_dft = proc(i)
   if multflag == 'fourth_iron':
      iron4_dft = proc(i)
   if multflag == 'full':
      full_dft = proc(i)

# Set up combinations of valences.
if options.valence == 'o':
   x = [[3,3,2,2], [3,2,3,2], [3,2,2,3], [2,3,3,2], [2,3,2,3], [2,2,3,3]]
elif options.valence == 'r':
   x = [[2,2,2,3], [2,2,3,2], [2,3,2,2], [3,2,2,2]]
else:
   sys.exit('Valence option must be passed. Use ' + sys.argv[0] + ' -h')

# For each possibility in newlist, modify the ironx_lists and ligand list charges.
listmap = { 0:iron1_list, 1:iron2_list, 2:iron3_list, 3:iron4_list, 4:lig_list, 5:iron1_dft, 6:iron2_dft, 7:iron3_dft, 8:iron4_dft, 9:full_dft }
for i in x:
   # Go through iron_lists, and modify name and Bq charges for this combination
   for j in [0,1,2,3]:
      temp = listmap[j].list[j][0:2]
      temp += str(i[j]) + ' ' + listmap[j].list[j][4:]
      listmap[j].list[j] = temp # For iron1, first atom is 'Fev' with v = valence. Just replace 'v' with 2/3
      for k in range(0,4):
         if k == j: continue
         temp = listmap[j].list[k][0:-2]
         temp += str(i[k]) + '\n'
         listmap[j].list[k] = temp # Assign the charge values to Bq for this iron
   # Now go through ligand and modify iron charges. The charges are in the same
   #   order as i and grouped. First two irons are H-cluster, so skip.
   for j in range(2, len(lig_list.list)):
      if lig_list.list[j][0:2] == 'Bq':
         for k in range(0,4):
            temp = lig_list.list[j+k][0:-2]
            temp += str(i[k]) + '\n'
            lig_list.list[j+k] = temp
         break

   # Set multiplicities in x_dft's
   for j in range(5,10):
      for k in xrange(len(listmap[j].list)):
         if RE1.search(listmap[j].list[k]):
            if j < 9:
               if i[j-5] == 3:
                  listmap[j].list[k] = re.sub('MULT [0-9]', 'MULT 6', listmap[j].list[k])
               elif i[j-5] == 2:
                  listmap[j].list[k] = re.sub('MULT [0-9]', 'MULT 5', listmap[j].list[k])
            else:
               if options.valence == 'o' and j == 9:
                  listmap[j].list[k] = re.sub('MULT [0-9][0-9]', 'MULT 20', listmap[j].list[k])
               elif options.valence == 'r' and j == 9:
                  listmap[j].list[k] = re.sub('MULT [0-9][0-9]', 'MULT 19', listmap[j].list[k])

   # Now open new file and write
   file_string = '41a1_422_63a' + str(i[0]) + '_64a' + str(i[1]) + \
                 '_65a' + str(i[2]) + '_66a' + str(i[3]) + '.nw'
   # Change start line in data
   start_string = 'start ' + file_string[0:-3] + '\n'
   refdata[0] = start_string

   # Start writing
   outfile = open(file_string, 'w')
   j = 0
   while j < len(refdata):
      if j == iron1_list.start:
         for l in xrange(len(listmap[0].list)):
            outfile.write(listmap[0].list[l])
         j += len(listmap[0].list)
      elif j == iron2_list.start:
         for l in xrange(len(listmap[1].list)):
            outfile.write(listmap[1].list[l])
         j += len(listmap[1].list)
      elif j == iron3_list.start:
         for l in xrange(len(listmap[2].list)):
            outfile.write(listmap[2].list[l])
         j += len(listmap[2].list)
      elif j == iron4_list.start:
         for l in xrange(len(listmap[3].list)):
            outfile.write(listmap[3].list[l])
         j += len(listmap[3].list)
      elif j == lig_list.start:
         for l in xrange(len(listmap[4].list)):
            outfile.write(listmap[4].list[l])
         j += len(listmap[4].list)
      elif j == iron1_dft.start:
         for l in xrange(len(listmap[5].list)):
            outfile.write(listmap[5].list[l])
         j += len(listmap[5].list)
      elif j == iron2_dft.start:
         for l in xrange(len(listmap[6].list)):
            outfile.write(listmap[6].list[l])
         j += len(listmap[6].list)
      elif j == iron3_dft.start:
         for l in xrange(len(listmap[7].list)):
            outfile.write(listmap[7].list[l])
         j += len(listmap[7].list)
      elif j == iron4_dft.start:
         for l in xrange(len(listmap[8].list)):
            outfile.write(listmap[8].list[l])
         j += len(listmap[8].list)
      elif j == full_dft.start:
         for l in xrange(len(listmap[9].list)):
            outfile.write(listmap[9].list[l])
         j += len(listmap[9].list)
      else:
         outfile.write(refdata[j])
         j += 1
   outfile.close()

   # Start writing
   os.mkdir(file_string[0:-3])
   shutil.move(file_string, file_string[0:-3])
   os.chdir(file_string[0:-3])
   pbs_new_file = open(start_string[5:].strip() + '.pbs', 'w')
   j = 0
   while j < len(pbsdata):
      if re.search('#PBS -N', pbsdata[j]):
         if options.valence == 'o':
            k = '#PBS -N HAox_12' + str(i[0]) + str(i[1]) + str(i[2]) + str(i[3]) + '\n'
         else:
            k = '#PBS -N HAred_12' + str(i[0]) + str(i[1]) + str(i[2]) + str(i[3]) + '\n'
      elif re.search('^JOBFILE', pbsdata[j]):
         k = 'JOBFILE=' + file_string + '\n'
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
   os.chdir('..')

