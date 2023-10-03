#!/uhome/cchang/python2.5/bin/python
# Script to check if all compounds have assigned concentrations, and to check
# for errors during the SBML read. CHC
import libsbml
reader = libsbml.SBMLReader()
document = reader.readSBML("merge_TTGF.xml")
document.printErrors()
model = document.getModel()
initial_assignments = model.getListOfInitialAssignments()
IA_symbol_list = []
for i in initial_assignments:
   IA_symbol_list.append(i.getSymbol())
rules = model.getListOfRules()
rule_variable_list = []
for i in rules:
   rule_variable_list.append(i.getVariable())
for i in model.getListOfSpecies():
   print i.getId(), i.getInitialConcentration()
   if i.getInitialConcentration() == '0.0':
      if (i.getId not in IA_symbol_list) and (i.getId not in rule_variable_list):
          print "There is no initial concentration or rule assigning one for " + \
                 i.getId()
