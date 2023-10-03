# Python script to create NWChem Prepare input decks for
# CpI QMMM jobs. CHC
import sys
import re
confstring = raw_input('Enter the redox state and quantum\
clusters in the format \'AA_AA_AA\', where A = O or R for\n\
oxidized or reduced cluster, and the clusters to be considered\n\
quantum are bracketed by underscores.\nPosition 1 = [2Fe]H\n\
Position 2 = bridging cubane\nPosition 3 = proximal cubane\n\
Position 4 = medial cubane\nPosition 5 = distal N-linked cubane\n\
Position 6 = [2Fe2S] cluster\n')
title = 'Prepare QM/MM calculation of CpI model ' + confstring + '\n'
quantum = 0
confdict = {}
counter = 1
for i in confstring:
   if i == '_' and quantum == 0: quantum = 1
   elif i == '_' and quantum == 1: quantum = 0
   else:
      confdict[counter] = (i, quantum)
      counter+=1
print confdict
F4Ocharges = {'C':-0.23650, 'H':0.11600, 'S':-0.54540} # Updated 4/2012
F4Rcharges = {'C':-0.82048, 'H':0.32061, 'S':-0.60058}
F2Ocharges = {'C':-0.19965, 'H':0.09630, 'S':-0.51570} # Updated 4/2012
F2Rcharges = {'C':-0.84492, 'H':0.33094, 'S':-0.37924}
FHO_Cyscharges = {'C':-0.17430, 'H':0.167125, 'S':-0.54140} # Updated 4/2012
FHO_Hischarges = {'CB':-0.35450, 'HB':0.183525, 'ND1':-0.22570, 'HD1':0.36460, 'CG':0.17700, 'CE1':-0.01430,\
                  'HE1':0.18260, 'NE2':-0.12700, 'CD2':-0.23810, 'HD2':0.18160} # Updated 4/2012
FHR_Cyscharges = {'C':-0.82155, 'H':0.33762, 'SG':-0.46598, 'Fe':0.80816, 'S':-0.86756}
FHR_Hischarges = {'CB':-0.70782, 'HB':0.36806, 'ND':-0.57492, 'HD1':0.43578, 'CG':0.07095, 'CE':0.21149,\
                  'HE':0.26477, 'NE':-0.56809, 'CD':-0.05102, 'HD2':0.25721}

bridging_res = [300, 355, 499, 503]
proximal_res = [157, 190, 193, 196]
medial_res = [147, 150, 153, 200]
distal_res = [94, 98, 101, 107]
fe2s2_res = [34, 46, 49, 62]

Cys_atoms = ['_CB', '2HB', '3HB', '_SG']
His_atoms = ['_CB', '2HB', '3HB', '_CG', '_ND1', '_HD1', '_NE2', '_CE1', '_HE1', '_CD2', '_HD2']

outfilename = confstring + '.nw'
outfile = open (outfilename, 'w')
outfile.write('start CpI_' + confstring + '_QMMM\n')
outfile.write('memory total 50 mw\nECHO\n')
outfile.write(title)
outfile.write('print medium\nset tolguess 1e-7\n\nprepare\n')
outfile.write('#--name of the pdb file\n   source built.pdb\n')
outfile.write('#--Default ionization state of histidines\n   histidine hid\n')
outfile.write('#--generate new topology and sequence file\n   new_top new_seq\n   amber\n')
outfile.write('#--generate new restart file\n   new_rst\n')
outfile.write('#--Specify protein-cluster bonds\n\
# [2Fe2S]\n\
   link 34:_SG 585:_FE2\n\
   link 46:_SG 585:_FE2\n\
   link 49:_SG 585:_FE1\n\
   link 62:_SG 585:_FE1\n\
# Distal\n\
   link 94:_NE2 584:_FE1\n\
   link 98:_SG 584:_FE3\n\
   link 101:_SG 584:_FE4\n\
   link 107:_SG 584:_FE2\n\
# Medial\n\
   link 147:_SG 583:_FE4\n\
   link 150:_SG 583:_FE2\n\
   link 153:_SG 583:_FE3\n\
   link 200:_SG 583:_FE1\n\
# Proximal\n\
   link 157:_SG 582:_FE2\n\
   link 190:_SG 582:_FE3\n\
   link 193:_SG 582:_FE1\n\
   link 196:_SG 582:_FE4\n\
# Bridging\n\
   link 300:_SG 581:_FE4\n\
   link 355:_SG 581:_FE1\n\
   link 499:_SG 581:_FE2\n\
   link 503:_SG 581:_FE3\n\
# H\n\
   link 503:_SG 580:_FE1\n')
outfile.write('# Modify cysteine charges to reflect charge transfer to clusters\n')
for i in fe2s2_res:
   if confdict[6][0] == 'O':
      for j in Cys_atoms:
         outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(F2Ocharges[j[1]]) + '\n')
   elif confdict[6][0] == 'R':
      for j in Cys_atoms:
         outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(F2Rcharges[j[1]]) + '\n')
for i in distal_res:
   if confdict[5][0] == 'O':
      if i == 94:
         for j in His_atoms:
            outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(FHO_Hischarges[j[1:]]) + '\n')
      else:
         for j in Cys_atoms:
            outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(FHO_Cyscharges[j[1]]) + '\n')
   elif confdict[5][0] == 'R':
      if i == 94:
         for j in His_atoms:
            outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(FHR_Hischarges[j[1:]]) + '\n')
      else:
         for j in Cys_atoms:
            outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(FHR_Cyscharges[j[1]]) + '\n')
for i in medial_res:
   if confdict[4][0] == 'O':
      for j in Cys_atoms:
         outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(F4Ocharges[j[1]]) + '\n')
   elif confdict[4][0] == 'R':
      for j in Cys_atoms:
         outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(F4Rcharges[j[1]]) + '\n')
for i in proximal_res:
   if confdict[3][0] == 'O':
      for j in Cys_atoms:
         outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(F4Ocharges[j[1]]) + '\n')
   elif confdict[3][0] == 'R':
      for j in Cys_atoms:
         outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(F4Rcharges[j[1]]) + '\n')
for i in bridging_res:
   if confdict[2][0] == 'O':
      for j in Cys_atoms:
         outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(F4Ocharges[j[1]]) + '\n')
   elif confdict[2][0] == 'R':
      for j in Cys_atoms:
         outfile.write('modify atom ' + str(i) + ':' + j + ' charge ' + str(F4Rcharges[j[1]]) + '\n')
outfile.write('#--define quantum region\n')
for i in confdict.iterkeys():
   if confdict[i][1] == 1:
      if i == 1: outfile.write('modify segment 580 quantum\n')
      elif i == 2:
         for j in bridging_res: outfile.write('modify segment ' + str(j) + ' quantum\n')
         outfile.write('modify segment 581 quantum\n')
      elif i == 3:
         for j in proximal_res: outfile.write('modify segment ' + str(j) + ' quantum\n')
         outfile.write('modify segment 582 quantum\n')
      elif i == 4:
         for j in medial_res: outfile.write('modify segment ' + str(j) + ' quantum\n')
         outfile.write('modify segment 583 quantum\n')
      elif i == 5:
         for j in distal_res: outfile.write('modify segment ' + str(j) + ' quantum\n')
         outfile.write('modify segment 584 quantum\n')
      elif i == 6:
         for j in fe2s2_res: outfile.write('modify segment ' + str(j) + ' quantum\n')
         outfile.write('modify segment 585 quantum\n')
outfile.close()
