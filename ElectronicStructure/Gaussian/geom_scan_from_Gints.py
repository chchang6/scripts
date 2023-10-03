#!/usr/bin/env python
# Script to match up internal coordinates from reactant, product, and TS optimizations
#   and create interpolation points.

import re

def cleanup_coords(arg1, arg2):
   # arg1 = 'R', 'T', or 'P'; needed to do the swapping if P
   # Product structure has (C3,O4) carbonyl swapped with (C7,O8) versus R and TS structures. Correct here.
   # arg2 = dict ((str)coordinate: (str)value)
   new_data = {}
   swapdict = {3:7, 4:8, 7:3, 8:4}
   swapdictkeylist = swapdict.keys()
   for i in arg2:
      t = re.sub('[()]', ' ', i)
      t = t.split(',')
      if t[0][0] == 'R':
         key_template = 'R( , )'
         t[0] = t[0].lstrip('R')
      elif t[0][0] == 'A':
         key_template = 'A( , , )'
         t[0] = t[0].lstrip('A')
      elif t[0][0] == 'L':
         key_template = 'L( , , , , )'
         t[0] = t[0].lstrip('L')
      else:
         key_template = 'D( , , , )'
         t[0] = t[0].lstrip('D')
      for j in xrange(len(t)):
         if arg1 == 'P' and int(t[j]) in swapdictkeylist:
            t[j] = swapdict[int(t[j])]
         else:
            t[j] = int(t[j])
      for j in t:
         key_template = re.sub(' ', str(j), key_template, 1)
      new_data[key_template] = arg2[i]
   return new_data

file = open('Hn9B7o.int', 'r')
data = file.readlines()
file.close()
reactant_data={}
for i in data:
   t = i.split()
   reactant_data[t[1]] = float(t[2])
reactant_data = cleanup_coords('R', reactant_data)

file = open('HIRSUc.int', 'r')
data = file.readlines()
file.close()
product_data = {}
for i in data:
   t = i.split()
   product_data[t[1]] = float(t[2])
product_data = cleanup_coords('P', product_data)

file = open('ElJg_2TS2_5.int', 'r')
data = file.readlines()
file.close()
TS_data = {}
for i in data:
   t = i.split()
   TS_data[t[1]] = float(t[2])
TS_data = cleanup_coords('T', TS_data)

reactant_keys = set(reactant_data.keys())
product_keys = set(product_data.keys())
TS_keys = set(TS_data.keys())
common_coors = reactant_keys & product_keys & TS_keys

# Sort keys with 3 passes through common_coors. If coordinate other than R, A, and D needed, increase accordingly.
sorted_CC = []
templist = []
for i in common_coors:
   t = re.sub('[()]', ' ', i)
   t = t.split(',')
   if t[0][0] == 'R':
      t[0] = t[0].lstrip('R')
      templist.append([ int(j) for j in t ])
sorted_CC.extend(sorted(templist))
templist = []
for i in common_coors:
   t = re.sub('[()]', ' ', i)
   t = t.split(',')
   if t[0][0] == 'A':
      t[0] = t[0].lstrip('A')
      templist.append([ int(j) for j in t ])
sorted_CC.extend(sorted(templist))
templist = []
for i in common_coors:
   t = re.sub('[()]', ' ', i)
   t = t.split(',')
   if t[0][0] == 'D':
      t[0] = t[0].lstrip('D')
      templist.append([ int(j) for j in t ])
sorted_CC.extend(sorted(templist))
sorted_keys = []
for i in sorted_CC:
   if len(i) == 2:
      sorted_keys.append('R(' + str(i[0]) + ',' + str(i[1]) + ')')
   elif len(i) == 3:
      sorted_keys.append('A(' + str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + ')')
   else:
      sorted_keys.append('D(' + str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + ',' + str(i[3]) +')')

# With properly sorted keys, calculate scan values for each internal coordinate
reactant_scan = {}
product_scan = {}
for key in sorted_keys:
   reactant_interval = (TS_data[key] - reactant_data[key])/4.
   product_interval = (product_data[key] - TS_data[key])/4.
   reactant_scan[key] = [reactant_data[key] + j*reactant_interval for j in xrange(5)]
   product_scan[key] = [TS_data[key] + j*product_interval for j in xrange(5)]
#DEBUG   if key == 'R(1,3)':
#DEBUG      print product_data[key]
#DEBUG      print key + str(reactant_scan[key]) + '\t' + str(product_scan[key])

# Write G09 input file for each scan point
# Get reference XYZ structure. Use reactant here. NOTE: Don't use product without swapping carbonyls!
XYZfile = open('Hn9B7o.xyz', 'r')
startXYZdata = XYZfile.readlines()
XYZfile.close()

for i in xrange(9):
   outfile = open('geom_scan_' + str(i) + '.gjf', 'w')
   outfile.write('%Chk=E008xt_' + str(i) + '.chk\n\n')
   outfile.write('#P BLYP/6-311++G(2df,p) DensityFit SCRF(Solvent=n-Octane) Opt=ModRedundant\n\n')
   outfile.write('Partial optimization for structure ' + str(i) + '\n\n0 1\n')
   for j in range(2,len(startXYZdata)):
      outfile.write(startXYZdata[j])
   outfile.write('\n')
   for j in sorted_keys:
      outstring = re.sub('R', 'B', j)
      outstring = re.sub('[(),]', ' ', outstring)
      outstring += '='
      outfile.write('%-15s\t' % (outstring))
      if i < 5:
         outfile.write('%10.5f ' % (reactant_scan[j][i]))  # This includes TS structure at end
      else:
         outfile.write('%10.5f ' % (product_scan[j][i-4]))
      outfile.write('F\n')
   outfile.write('\n')
   outfile.close()
