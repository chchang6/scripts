#!/uhome/cchang/python2.5/bin/python
# Script to check if all compounds have assigned concentrations, and to check
# for errors during the SBML read. CHC
import libsbml
reader = libsbml.SBMLReader()
document = reader.readSBML("merge_TTGF.xml")
#document.printErrors()
model = document.getModel()
# Modify unit definitions involving umole
old_unit_list = ['umole', 'per_uM_per_s', 'per_uM', 'per_uM_2_per_s', 'per_umol2_per_s', 'uM', 'uM_squared', 'uM_per_s']
new_unit_list = ['mmole', 'per_mM_per_s', 'per_mM', 'per_mM_2_per_s', 'per_mmol2_per_s', 'mM', 'mM_squared', 'mM_per_s']
model_unitdef_list = model.getListOfUnitDefinitions()
for i in model_unitdef_list:
   libsbml.UnitDefinition.printUnits(i)
for i in model_unitdef_list:
   for j in old_unit_list:
      if i.getId() == j:
         i.setId(new_unit_list[ old_unit_list.index(j) ])
         i.setName(new_unit_list[ old_unit_list.index(j) ])
         unitlist = i.getListOfUnits()
         for k in unitlist:
            if k.isMole():
               k.setScale(-3)
# Go through species, and change units
species = model.getListOfSpecies()
for i in species:
   if i.getSubstanceUnits() == 'umole':
      i.setSubstanceUnits('mmole')
      if i.isSetInitialConcentration() == True:
         temp = i.getInitialConcentration()
         i.setInitialConcentration( temp/1000 )
parameters = model.getListOfParameters()
for i in parameters:
   in_unit = i.getUnits()
   if in_unit == 'per_uM_per_s':
      i.setUnits('per_mM_per_s')
      if i.isSetValue() == True:
         temp = i.getValue()
         i.setValue( temp/1000 )
   elif in_unit == 'umole':
      i.setUnits('mmole')
      if i.isSetValue() == True:
         temp = i.getValue()
         i.setValue( temp/1000 )
   elif in_unit == 'per_uM':
      i.setUnits('per_mM')
      if i.isSetValue() == True:
         temp = i.getValue()
         i.setValue( temp/1000 )
   elif in_unit == 'per_uM_2_per_s':
      i.setUnits('per_mM_2_per_s')
      if i.isSetValue() == True:
         temp = i.getValue()
         i.setValue( temp/1e6 )
   elif in_unit == 'per_umol2_per_s':
      i.setUnits('per_mmol_2_per_s')
      if i.isSetValue() == True:
         temp = i.getValue()
         i.setValue( temp/1e6 )
   elif in_unit == 'uM':
      i.setUnits('mM')
      if i.isSetValue() == True:
         temp = i.getValue()
         i.setValue( temp/1000 )
   elif in_unit == 'uM_squared':
      i.setUnits('mM_squared')
      if i.isSetValue() == True:
         temp = i.getValue()
         i.setValue( temp/1000 )
   elif in_unit == 'uM_per_s':
      i.setUnits('mM_per_s')
      if i.isSetValue() == True:
         temp = i.getValue()
         i.setValue( temp/1000 )
writer = libsbml.SBMLWriter()
out_model =  writer.writeSBML(document, "test.xml")
