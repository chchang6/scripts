#!/usr/bin/env python
from scipy.linalg import norm
import os, sys, numpy, re

# Regular expression to remove percentage from hybridization strings
regex1=re.compile(r'\([ 0-9\.]{6}%\)')
# Function definitions
def BondOrderMatrixReader(start):
   global NumberOfAtoms, InfileData
# Assume NBO outputs 9 columns of indices per row.
   i=NumberOfAtoms//8 # Number of complete blocks.
   remainder=NumberOfAtoms%9 # Number of remaining columns
   x=numpy.zeros((NumberOfAtoms,NumberOfAtoms))
   j=0 # Counter for complete blocks
   while(j<i):
      k=0 # Counter for atoms in block
      while k < NumberOfAtoms:
         temp=InfileData[start+j*(NumberOfAtoms+3)+k].split()
         for l in xrange(0,9): # xrange excludes top limit
            x[k,j*9+l]=float(temp[l+2])
         k += 1
      j += 1
   # Read in remainder
   k=0
   while(k<NumberOfAtoms):
      temp=InfileData[start+i*(NumberOfAtoms+3)+k].split()
      for l in xrange(0,remainder): # xrange excludes top limit
         x[k,i*9+l]=float(temp[l+2])
      k += 1
   # Extract relevant bond orders
   BondList=[]
   # Add metal-ligand bond orders
   for i in dictionary.iterkeys():
      for j in dictionary[i]:
         BondList.append(int(i))
         BondList.append(int(j))
         BondList.append(x[int(i)-1,int(j)-1])
   # Add metal-metal bond orders
   i = dictionary.keys()
   for j in range (0,len(i)-1): # Last anchor point one from end of list w/ index len-2
      for k in range (1,len(i)): # Last sampling point = last list element, w/ index len-1
         BondList.append(int(i[j]))
         BondList.append(int(i[k]))
         BondList.append(x[int(i[j])-1,int(i[k])-1])
   return BondList

def ElementReader(start,column):
   global NumberOfAtoms, InfileData
   Elements=[]
   i=0
   while(i<NumberOfAtoms):
      temp=InfileData[start+i].split(None)
      Elements.append(temp[column])
      i += 1
   return Elements

def BondOrderTotalReader(start,column):
   global NumberOfAtoms, InfileData
   BOT=[]
   i=0
   while(i<NumberOfAtoms):
      temp=InfileData[start+i].split(None)
      BOT.append(float(temp[column]))
      i += 1
   return BOT

def NBO_Covalency(start,end):
   global InfileData, dictionary
   NBO_List=[]
   i=start
   j=0
   while(i < end):
      Line=InfileData[i]
      if Line[3]!=' ':                   # Line starts an NBO
         # Does NBO have metal contribution?
         if dictionary.has_key(Line[26:28].lstrip()) or \
            dictionary.has_key(Line[32:34].lstrip()) or \
            dictionary.has_key(Line[38:40].lstrip()):
            if Line[16:18] == 'BD': j=2        # j counter for number of hybrids.
            elif Line[16:18] == '3C': j=3
            #else: continue             # Discard LP and CR
         if j==2:
            x=NBO(Line)   # This NBO is a metal-ligand 2C bond
            k=1
            while k >= 1:
               Line2=InfileData[i+k]
               if Line2[16:22]!='      ':
                  if k>1:
                     x.Percent[1]=float(Line2[16:22])    # Second hybrid scanned
                     x.Hybrid[1]=Line2[34:]
                     if InfileData[i+k+1][50] == 'f':x.Hybrid[1]=x.Hybrid[1]+InfileData[i+k+1][50:]
                     x.Hybrid[1]=regex1.sub('',x.Hybrid[1])
                     if Line2[26] == '-': x.Percent[1] = -1. * x.Percent[1]
                     k=-1
                  else:
                     x.Percent[0]=float(Line2[16:22])    # First hybrid scanned
                     x.Hybrid[0]=Line2[34:]
                     if InfileData[i+k+1][50] == 'f':x.Hybrid[0]=x.Hybrid[0]+InfileData[i+k+1][50:]
                     x.Hybrid[0]=regex1.sub('',x.Hybrid[0])
                     if Line2[26] == '-': x.Percent[0] = -1. * x.Percent[0]
               k += 1
            NBO_List.append(x)
         elif j==3:
            x=NBO(Line)   # This NBO is a metal-ligand 3C bond
            k=1
            while k >= 1:
               Line2=InfileData[i+k]
               if Line2[16:22] != '      ':
                  if j==1:            # Last hybrid scanned
                     x.Percent[2]=float(Line2[16:22])
                     x.Hybrid[2]=Line2[34:]
                     if InfileData[i+k+1][50]=='f':x.Hybrid[2]=x.Hybrid[2]+InfileData[i+k+1][50:]
                     x.Hybrid[2]=regex1.sub('',x.Hybrid[2])
                     if Line2[26]=='-': x.Percent[2] = -1. * x.Percent[2]
                     j = 0
                     k=-1
                  elif j==2:         # Second hybrid scanned
                     x.Percent[1]=float(Line2[16:22])
                     x.Hybrid[1]=Line2[34:]
                     if InfileData[i+k+1][50]=='f':x.Hybrid[1]=x.Hybrid[1]+InfileData[i+k+1][50:]
                     x.Hybrid[1]=regex1.sub('',x.Hybrid[1])
                     if Line2[26]=='-': x.Percent[1] = -1. * x.Percent[1]
                     j -= 1
                  else:                # First hybrid scanned
                     x.Percent[0]=float(Line2[16:22])
                     x.Hybrid[0]=Line2[34:]
                     if InfileData[i+k+1][50]=='f':x.Hybrid[0]=x.Hybrid[0]+InfileData[i+k+1][50:]
                     x.Hybrid[0]=regex1.sub('',x.Hybrid[0])
                     if Line2[26]=='-': x.Percent[0] = -1. * x.Percent[0]
                     j -= 1
               k += 1
            # Need to check that the order of NBOs is (ligand1, metal, ligand2), i.e. metal is in center. If not, reshuffle.
            if dictionary.has_key(x.Atom1.strip()) and dictionary.has_key(x.Atom2.strip()): # Two metals as atoms 1 and 2
               try:
                  dictionary[x.Atom1.strip()].index(x.Atom3.strip()) # Atom 3 is a ligand to atom 1, switch order
                  x.Atom1, x.Atom2 = x.Atom2, x.Atom1
                  x.Percent[0], x.Percent[1] = x.Percent[1], x.Percent[0]
                  x.Hybrid[0], x.Hybrid[1] = x.Hybrid[1], x.Hybrid[0]
               except ValueError: # Atom 3 is a ligand to atom 2, leave order as is.
                  pass
            elif dictionary.has_key(x.Atom1.strip()) and dictionary.has_key(x.Atom3.strip()): # Two metals as atoms 1 and 3
               try:
                  dictionary[x.Atom1.strip()].index(x.Atom2.strip()) # Atom 2 is a ligand to atom 1, switch atoms 1 and 2
                  x.Atom1, x.Atom2 = x.Atom2, x.Atom1
                  x.Percent[0], x.Percent[1] = x.Percent[1], x.Percent[0]
                  x.Hybrid[0], x.Hybrid[1] = x.Hybrid[1], x.Hybrid[0]
               except ValueError: # Atom 2 is a ligand to atom 3, switch atoms 2 and 3
                  x.Atom2, x.Atom3 = x.Atom3, x.Atom2
                  x.Percent[1], x.Percent[2] = x.Percent[2], x.Percent[1]
                  x.Hybrid[1], x.Hybrid[2] = x.Hybrid[2], x.Hybrid[1]
            elif dictionary.has_key(x.Atom2.strip()) and dictionary.has_key(x.Atom3.strip()): # Two metals as atoms 2 and 3
               try:
                  dictionary[x.Atom2.strip()].index(x.Atom1.strip()) # Atom 1 is a ligand to atom 2, leave as is
                  pass
               except ValueError: # Atom 1 is a ligand to atom 3, switch atoms 2 and 3
                  x.Atom2, x.Atom3 = x.Atom3, x.Atom2
                  x.Percent[1], x.Percent[2] = x.Percent[2], x.Percent[1]
                  x.Hybrid[1], x.Hybrid[2] = x.Hybrid[2], x.Hybrid[1]
            elif dictionary.has_key(x.Atom1.strip()) and not (dictionary.has_key(x.Atom2.strip()) or dictionary.has_key(x.Atom3.strip())): # Metal is first atom, no other metals
               x.Atom1, x.Atom2 = x.Atom2, x.Atom1
               x.Percent[0], x.Percent[1] = x.Percent[1], x.Percent[0]
               x.Hybrid[0], x.Hybrid[1] = x.Hybrid[1], x.Hybrid[0]
            elif dictionary.has_key(x.Atom3.strip()) and not (dictionary.has_key(x.Atom1.strip()) or dictionary.has_key(x.Atom2.strip())): # Metal is third and only atom
               x.Atom3, x.Atom2 = x.Atom2, x.Atom3
               x.Percent[2], x.Percent[1] = x.Percent[1], x.Percent[2]
               x.Hybrid[2], x.Hybrid[1] = x.Hybrid[1], x.Hybrid[2]
            NBO_List.append(x)
         j = 0
      i += 1
      #continue
   else:
      i += 1
   for i in NBO_List:
      if i.Type=='BD ' or i.Type=='BD*':
         try:
            sign=i.Percent[0]*i.Percent[1]/abs(i.Percent[0]*i.Percent[1])
         except(ZeroDivisionError):
            sign=1.
         i.Covalency[0]=min(abs(i.Percent[0]),abs(i.Percent[1])) / \
                        max(abs(i.Percent[0]),abs(i.Percent[1])) * \
                        i.Occupancy * sign
      elif i.Type=='3C ' or i.Type=='3C*':
         try:
            sign01=i.Percent[0]*i.Percent[1]/abs(i.Percent[0]*i.Percent[1])
         except(ZeroDivisionError):
            sign01=1.
         try:
            sign21=i.Percent[2]*i.Percent[1]/abs(i.Percent[2]*i.Percent[1])
         except(ZeroDivisionError):
            sign21=1. 
         if (abs(i.Percent[0]) > abs(i.Percent[1]) and \
             abs(i.Percent[2]) > abs(i.Percent[1])):
            i.Covalency[0]=abs(i.Percent[0])/(abs(i.Percent[0]) + abs(i.Percent[2])) * \
                           abs(i.Percent[1]/100) * i.Occupancy * sign01
            i.Covalency[1]=abs(i.Percent[2])/(abs(i.Percent[0]) + abs(i.Percent[2])) * \
                           abs(i.Percent[1]/100) * i.Occupancy * sign21
         elif (abs(i.Percent[0]) > abs(i.Percent[1]) and \
               abs(i.Percent[2]) < abs(i.Percent[1])):
            i.Covalency[0]=abs(abs(i.Percent[1]) - abs(i.Percent[2]))/100 * \
                           i.Occupancy * sign01
            i.Covalency[1]=abs(i.Percent[2])/100 * i.Occupancy * sign21
         elif(abs(i.Percent[0]) < abs(i.Percent[1]) and \
              abs(i.Percent[2]) > abs(i.Percent[1])):
            i.Covalency[0]=abs(i.Percent[0])/100 * i.Occupancy * sign01
            i.Covalency[1]=abs(abs(i.Percent[1]) - abs(i.Percent[0]))/100 * i.Occupancy * sign21
         else:
            i.Covalency[0]=abs(i.Percent[0])/100 * i.Occupancy * sign01
            i.Covalency[1]=abs(i.Percent[2])/100 * i.Occupancy * sign21
   return NBO_List

def LMCT_Covalency(start,end):
   global InfileData, dictionary, LigandIndicesList
   NLMO_List = []
   i = start
   while (i < end):
      Line=InfileData[i]
      if Line[3]!=' ':                   # Line starts an NLMO
         if Line[27:29]=='LP':     # Lone pairs only
            if int(Line[37:39]) in LigandIndicesList:   # Lone pair is a ligand atom
               x = NLMO(Line)
               k = 1
               while InfileData[i+k][3]==' ':
                  AtomIndex=InfileData[i+k][37:39]
                  if AtomIndex.strip() in dictionary.keys():
                     x.AtomList.append(InfileData[i+k][34:39])
                     x.PercentList.append(float(InfileData[i+k][26:32]) / 100)
                  k+=1
                  if i+k==end: break
               NLMO_List.append(x)
      i +=1
   return NLMO_List
      
def MLCT_Covalency(start,end):
   global InfileData, dictionary
   NLMO_List = []
   i = start
   while (i < end):
      Line=InfileData[i]
      if Line[3] != ' ':                 # Line starts an NLMO
         if Line[27:29]=='LP':     # Lone pairs only
            if Line[37:39].strip() in dictionary.keys():   # Lone pair is a ligand atom
               x = NLMO(Line)
               k = 1
               while InfileData[i+k][3]==' ':
                  AtomIndex=InfileData[i+k][37:39]
                  if AtomIndex.strip() in dictionary[Line[37:39].strip()]:
                     x.AtomList.append(InfileData[i+k][34:39])
                     x.PercentList.append(float(InfileData[i+k][27:32]) / 100)
                  k+=1
               NLMO_List.append(x)
      i +=1
   return NLMO_List

def GeometryMatrix(start):
   global InfileData
   i=0; temp=numpy.zeros((NumberOfAtoms,3))
   while i < NumberOfAtoms:
      line=InfileData[start + i].split(None)
      temp[i,0]=float(line[3])
      temp[i,1]=float(line[4])
      temp[i,2]=float(line[5])
      i += 1
   return temp
   
# Class definitions
class NBO:
   def __init__(self,string):
      self.Index=string[0:4]
      self.Occupancy=float(string[7:14])
      self.Type=string[16:19]
      self.Name=string[16:41]
      if self.Type=='BD ' or self.Type=='BD*':
         self.Atom1=string[26:28]
         self.Atom2=string[32:34]
         self.Percent=[0.0,0.0]
         self.Hybrid=['a','b']
         self.Covalency=[0.0]
      else:
         self.Atom1=string[26:28]
         self.Atom2=string[32:34]
         self.Atom3=string[38:40]
         self.Percent=[0.0,0.0,0.0]
         self.Hybrid=['a','b','c']
         self.Covalency=[0.0,0.0]
         
class NLMO:
   def __init__(self,string):
      self.Index=string[0:4]
      self.Name=string[27:39]
      self.ParentPercentage=string[17:25]
      self.AtomList=[]
      self.PercentList=[]
      
# For testing...
#InfileName="SVWN5_alltermCO.out"
#NumberOfAtoms=29
dictionary={'7':['1','9','10','16','17','18'], '8':['9','10','18','19','20','29']}
# ...or get data from user
InfileName=raw_input("Enter the name of the file containing NBO output:")
NumberOfAtoms=int(raw_input("Enter the number of atoms in the complex:"))
#MetalsString=raw_input("Enter a comma-separated list of atom indices \
#corresponding to the metal ions:")
#MetalsList=MetalsString.split(',')
#dictionary={}
#for i in MetalsList:
#   query_string='Enter a comma-separated list of atom indices \
#corresponding to ligand atoms for metal ' + i + ' :'
#   Ligand_i_String=raw_input(query_string)
#   Ligand_i_List=Ligand_i_String.split(',')
#   dictionary[i]=Ligand_i_List
# Now create unique sorted list of ligand indices
LigandIndicesList=dictionary.values()
i=1
while i<len(LigandIndicesList):
   LigandIndicesList[0]=LigandIndicesList[0]+LigandIndicesList[i]
   i += 1
LigandIndicesList = list(set(LigandIndicesList[0]))
temp2=[]
for i in range(0,len(LigandIndicesList)): temp2.append(int(LigandIndicesList[i]))
temp2.sort()
LigandIndicesList=temp2

MetalIndicesList=dictionary.keys()
for i in MetalIndicesList:
   i = int(i)
MetalIndicesList.sort()

# Read in NBO output file data
Infile=open(os.path.join(os.getcwd(),InfileName),'r')
InfileData=Infile.readlines()
Infile.close()
templist=[]
for i in InfileData:
   templist.append(i.rstrip())
InfileData=templist
templist=[]

# Set logical flags to false; these are necessary so only the first instance
# of certain data blocks is read.
NPA_TableTruth=False
WibergMatrixTruth=False
WibergTotalsTruth=False
AAOWNAO_MatrixTruth=False
AAOWNAO_TotalsTruth=False
MO_MatrixTruth=False
MO_TotalsTruth=False
NPA_ElectronConfigTruth=False

# Establish useful reference line numbers in file
for Index, Line in enumerate(InfileData):
# Data prior to NBO analysis section
   if Line[25:46]=='Standard orientation:':
      CoordinateStart=Index+5
   if Line==' Mulliken atomic charges:':
      MullikenStart=Index+2
# Data prior to separate alpha and beta sections
   if (Line==' Summary of Natural Population Analysis:' and not NPA_TableTruth):
      NPA_TableTruth=True
      NPA_TableStart=Index+6
   if (Line[28:49]=='Electron Configuration' and not NPA_ElectronConfigTruth):
      NPA_ElectronConfigTruth=True
      NPA_ElectronConfigStart=Index+2
   if (Line==' Wiberg bond index matrix in the NAO basis:' and not WibergMatrixTruth):
      WibergMatrixTruth=True
      WibergMatrixStart=Index+4
   if (Line==' Wiberg bond index, Totals by atom:' and not WibergTotalsTruth):
      WibergTotalsTruth=True
      WibergTotalsStart=Index+4
   if (Line==' Atom-atom overlap-weighted NAO bond order:' and not AAOWNAO_MatrixTruth):
      AAOWNAO_MatrixTruth=True
      AAOWNAO_MatrixStart=Index+4
   if (Line==' Atom-atom overlap-weighted NAO bond order, Totals by atom:' and not AAOWNAO_TotalsTruth):
      AAOWNAO_TotalsTruth=True
      AAOWNAO_TotalsStart= Index+4
   if (Line==' MO bond order:' and not MO_MatrixTruth):
      MO_MatrixTruth=True
      MO_MatrixStart=Index+4
   if (Line==' MO atomic valencies:' and not MO_TotalsTruth):
      MO_TotalsTruth=True
      MO_TotalsStart=Index+4
# Starts of alpha and beta sections
   if Line==' *******         Alpha spin orbitals         *******':
      AlphaStart=Index
   if Line==' *******         Beta  spin orbitals         *******':
      BetaStart=Index

# Need to start over again so we can reference the alpha and
# beta starting line values
for Index,Line in enumerate(InfileData):
   if (Line[0:18]=='   Total non-Lewis'):
      if (Index< BetaStart):
         AlphaNBO_Start=Index+5
      else:
         BetaNBO_Start=Index+5
   if (Line[1:19]=='NHO DIRECTIONALITY'):
      if (Index< BetaStart):
         AlphaNBO_End=Index-2
      else:
         BetaNBO_End=Index-2
   if Line[1:27]=='Hybridization/Polarization':
      if(Index< BetaStart):
         AlphaNLMO_Start=Index+2
      else:
         BetaNLMO_Start=Index+2
   if Line[1:27]=='Individual LMO bond orders':
      if(Index< BetaStart):
         AlphaNLMO_End=Index-2
      else:
         BetaNLMO_End=Index-2
   if Line[0:43]==' Atom-Atom Net Linear NLMO/NPA Bond Orders:':
      if(Index< BetaStart):
         AlphaNLMONPA_MatrixStart=Index+4
      else:
         BetaNLMONPA_MatrixStart=Index+4
   if Line==' Linear NLMO/NPA Bond Orders, Totals by Atom:':
      if(Index< BetaStart):
         AlphaNLMONPA_TotalsStart=Index+4
      else:
         BetaNLMONPA_TotalsStart=Index+4

# Main
Cartesians=GeometryMatrix(CoordinateStart)
Elements=ElementReader(MullikenStart,1)
Indices=ElementReader(MullikenStart,0)
MullikenCharges=BondOrderTotalReader(MullikenStart,2)
NPA_Charges=BondOrderTotalReader(NPA_TableStart,2)
NPA_SMD=BondOrderTotalReader(NPA_TableStart,7)
Wiberg=BondOrderMatrixReader(WibergMatrixStart)
WibergTotals=BondOrderTotalReader(WibergTotalsStart,2)
AAOWNAO=BondOrderMatrixReader(AAOWNAO_MatrixStart)
AAOWNAO_Totals=BondOrderTotalReader(AAOWNAO_TotalsStart,2)
MO=BondOrderMatrixReader(MO_MatrixStart)
MO_Totals=BondOrderTotalReader(MO_TotalsStart,2)
alpha_NLMONPA=BondOrderMatrixReader(AlphaNLMONPA_MatrixStart)
alpha_NLMONPA_Totals=BondOrderTotalReader(AlphaNLMONPA_TotalsStart,2)
beta_NLMONPA=BondOrderMatrixReader(BetaNLMONPA_MatrixStart)
beta_NLMONPA_Totals=BondOrderTotalReader(BetaNLMONPA_TotalsStart,2)
alpha_NBOcov=NBO_Covalency(AlphaNBO_Start,AlphaNBO_End) 
beta_NBOcov=NBO_Covalency(BetaNBO_Start,BetaNBO_End)
alpha_LMCT=LMCT_Covalency(AlphaNLMO_Start,AlphaNLMO_End)
beta_LMCT=LMCT_Covalency(BetaNLMO_Start,BetaNLMO_End)
alpha_MLCT=MLCT_Covalency(AlphaNLMO_Start,AlphaNLMO_End)
beta_MLCT=MLCT_Covalency(BetaNLMO_Start,BetaNLMO_End)

# Generate Charges and Bond Orders report
Outfile=open(os.path.join(os.getcwd(),'qBO.csv'),'w')
Outfile.write("NPA Analysis\n")
Outfile.write("Atom, Mulliken charge, NPA charge, spin, Wiberg totals, NAOBO totals, MO atomic valencies, NLMO/NPA\n")
for i in range(0,NumberOfAtoms):
   tempstring=Elements[i] + str(Indices[i]) + "," + str(MullikenCharges[i]) + "," + str(NPA_Charges[i]) + \
              "," + str(NPA_SMD[i]) + "," + str(WibergTotals[i]) + "," + str(AAOWNAO_Totals[i]) + "," + \
              str(MO_Totals[i]) + "," + str(alpha_NLMONPA_Totals[i]+beta_NLMONPA_Totals[i]) + "\n"
   Outfile.write(tempstring)
Outfile.write("\n")
Outfile.write("\n")
Outfile.write('Bond, Wiberg BO, NAOBO, MOBO, NLMO/NPA BO, Distance(Angstroms)\n')
i=0
while(i<len(Wiberg)/3):
   tempstring = Elements[Wiberg[i*3+0]-1] + str(Wiberg[i*3+0]) + "-" + Elements[Wiberg[i*3+1]-1] + \
                str(Wiberg[i*3+1]) + "," + str(Wiberg[i*3+2]) + "," + str(AAOWNAO[i*3+2]) + "," + \
                str(MO[i*3+2]) + "," + str(alpha_NLMONPA[i*3+2] + beta_NLMONPA[i*3+2]) + \
 "," + str(norm(numpy.array(Cartesians[Wiberg[i*3+0]-1],)-numpy.array(Cartesians[Wiberg[i*3+1]-1],))) + "\n"
   Outfile.write(tempstring)
   i+=1
Outfile.close()

# Generate Covalency report
Outfile=open(os.path.join(os.getcwd(),'covalency.csv'),'w')
#Outfile.write(u'\x03B1 BD, 3C\n')
Outfile.write('alpha BD and 3C\n')
Outfile.write("NBO index, NBO, occupancy, % ligand, % metal, % 3C, ligand hybridization, \
metal hybridization, 3C hybridization, Covalency Ligand, Covalency 3C\n")
for i in alpha_NBOcov:
   tempstring = str(i.Index) + "," + i.Name + "," + str(i.Occupancy) + ","
   Outfile.write(tempstring)
   if i.Type=='BD ' or i.Type=='BD*':
      if dictionary.has_key(i.Atom1.strip()): # Metal is first atom
         tempstring=str(i.Percent[1]) + "," + str(i.Percent[0]) + ",," + \
                    i.Hybrid[1] + "," + i.Hybrid[0] + ",," + str(i.Covalency[0]) + "\n"
      else:
         tempstring=str(i.Percent[0]) + "," + str(i.Percent[1]) + ",," + \
                    i.Hybrid[0] + "," + i.Hybrid[1] + ",," + str(i.Covalency[0]) + "\n"
   elif i.Type=='3C ' or i.Type=='3C*':  # L-M-3 order already established
                                         # during covalency calculation
      tempstring=str(i.Percent[0]) + "," + str(i.Percent[1]) + "," + \
                 str(i.Percent[2]) + "," + i.Hybrid[0] + "," + \
                 i.Hybrid[1] + "," + i.Hybrid[2] + "," + \
                 str(i.Covalency[0]) + "," + str(i.Covalency[1]) + "\n"
   Outfile.write(tempstring)
Outfile.write("\n")
Outfile.write("\n")
Outfile.write("3-center hyperbonding, Centers, %A-B, %B-C, occupancy, NBOs (A-B:C), NHOs (A: B: C)\n")
Outfile.write("enter any 3CHB here\n")
Outfile.write("\n")
Outfile.write("\n")

# Print MLCT header
Outfile.write("M LP NLMO, % parent NBO, Type parent NBO, ")
i=0
tempstring=''
while i < len(LigandIndicesList):
   tempstring=tempstring + "e- " + Elements[LigandIndicesList[i]-1] + str(LigandIndicesList[i]) + ","
   i += 1
Outfile.write(tempstring)
Outfile.write("\n")

# Print MLCT values. Will have to hand edit to line up with headers.
for i in alpha_MLCT:
   tempstring=i.Index + "," + i.ParentPercentage + "," + i.Name
   Outfile.write(tempstring)
   tempstring=','
   for j,k in zip(i.AtomList, i.PercentList):
      tempstring=tempstring + ',' + str(j) + ',' + str(k)
   Outfile.write(tempstring)
   Outfile.write("\n")

# Print leftmost metal atom labels for MLCT summary lines
for i in MetalIndicesList:
   tempstring=",," + Elements[int(i)-1] + str(i) + " MLCT\n"
   Outfile.write(tempstring)
Outfile.write("\n")

# Print LMCT header
Outfile.write("Ligand LP NLMO,,,")
tempstring=''
for i in MetalIndicesList:
   tempstring=tempstring + 'e- ' + Elements[int(i)-1] + str(i) + ","
Outfile.write(tempstring)
Outfile.write("\n")

# Print LMCT values. Will have to hand edit.
for i in alpha_LMCT:
   tempstring=str(i.Index) + "," + i.ParentPercentage + "," + i.Name + ","
   Outfile.write(tempstring)
   tempstring=''
   for j,k in zip(i.AtomList,i.PercentList):
      tempstring=tempstring + j + "," + str(k) + ","
   Outfile.write(tempstring)
   Outfile.write("\n")
Outfile.write(",,Covalency:\n")
Outfile.write("\n")

# Print beta section
Outfile.write('Beta BD and 3C\n')
Outfile.write("NBO index, NBO, occupancy, % ligand, % metal, % 3C, ligand hybridization, metal hybridization, 3C hybridization, Covalency Ligand, Covalency 3C\n")
for i in beta_NBOcov:
   tempstring=str(i.Index) + "," + i.Name + "," + str(i.Occupancy) + ","
   Outfile.write(tempstring)
   if i.Type=='BD ' or i.Type=='BD*':
      if dictionary.has_key(i.Atom1.strip()): # Metal is first atom
         tempstring=str(i.Percent[1]) + "," + str(i.Percent[0]) + \
                    ",," + i.Hybrid[1] + "," + i.Hybrid[0] + ",," + \
                    str(i.Covalency[0]) + "\n"
      else:
         tempstring=str(i.Percent[0]) + "," + str(i.Percent[1]) + ",," + \
                    i.Hybrid[0] + "," + i.Hybrid[1] + ",," + \
                    str(i.Covalency[0]) + "\n"
   elif i.Type=='3C ' or i.Type=='3C*':  # L-M-3 order already established during covalency calculation
      tempstring=str(i.Percent[0]) + "," + str(i.Percent[1]) + "," + \
                 str(i.Percent[2]) + "," + i.Hybrid[0] + "," + \
                 i.Hybrid[1] + "," + i.Hybrid[2] + "," + \
                 str(i.Covalency[0]) + "," + str(i.Covalency[1]) + "\n"
   Outfile.write(tempstring)
Outfile.write("\n")
Outfile.write("\n")
Outfile.write("3-center hyperbonding, Centers, %A-B, %B-C, occupancy, NBOs (A-B:C), NHOs (A: B: C)\n")
Outfile.write("enter any 3CHB here\n")
Outfile.write("\n")
Outfile.write("\n")

# Print MLCT header
Outfile.write("M LP NLMO, % parent NBO, Type parent NBO, ")
i=0
while i < len(LigandIndicesList):
   tempstring="e- " + Elements[LigandIndicesList[i]-1] + str(LigandIndicesList[i]) + ","
   Outfile.write(tempstring)
   i += 1
Outfile.write("\n")

# Print MLCT values. Will have to hand edit to line up with headers.
for i in beta_MLCT:
   tempstring=i.Index + "," + i.ParentPercentage + "," + i.Name
   Outfile.write(tempstring)
   tempstring=','
   for j,k in zip(i.AtomList, i.PercentList):
      tempstring=tempstring + ',' + str(j) + ',' + str(k)
   Outfile.write(tempstring)
   Outfile.write("\n")

# Print leftmost metal atom labels for MLCT summary lines
for i in MetalIndicesList:
   tempstring=",," + Elements[int(i)-1] + str(i) + " MLCT\n"
   Outfile.write(tempstring)
Outfile.write("\n")

# Print LMCT header
Outfile.write("Ligand LP NLMO,,,")
for i in MetalIndicesList:
   tempstring="e- " + Elements[int(i)-1] + str(i) + ","
   Outfile.write(tempstring)
Outfile.write("\n")

# Print LMCT values. Will have to hand edit.
for i in beta_LMCT:
   tempstring=str(i.Index) + "," + i.ParentPercentage + "," + i.Name + ","
   Outfile.write(tempstring)
   tempstring=''
   for j,k in zip(i.AtomList,i.PercentList):
      tempstring=tempstring + j + "," + str(k) + ","
   Outfile.write(tempstring)
   Outfile.write("\n")
Outfile.write(",,Covalency:\n")
Outfile.write("\n")

Outfile.close()
