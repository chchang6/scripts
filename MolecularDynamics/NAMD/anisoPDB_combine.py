#!/usr/bin/python
import os,sys
PDB_file = open('test.pdb', 'r')
PDB_record_list = PDB_file.readlines()
PDB_file.close()
PDB_record_list.pop(0)
PDB_record_list.pop(-1)
ANISO_file = open('aniso.log', 'r')
ANISO_record_list = ANISO_file.readlines()
ANISO_file.close()
outfile = open('combined.pdb', 'w')
for i,j in zip(PDB_record_list,ANISO_record_list):
   correct_number=j[6:11]
   new_PDB_line=i[0:6] + correct_number + i[11:]
   new_aniso_line=j[0:6] + correct_number + i[11:31] + j[31:72] + i[72:]
   outfile.write(new_PDB_line.lstrip())
   outfile.write(new_aniso_line.lstrip())
outfile.write('END')
outfile.close()
