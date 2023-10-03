#!/uhome/cchang/python2.5/bin/python
# Script to check if all compounds have assigned concentrations, and to check
# for errors during the SBML read. CHC
import libsbml
reader = libsbml.SBMLReader()
document = reader.readSBML("C_rein_TCA_v2.3.xml")
#document.printErrors()
model = document.getModel()
# Modify unit definitions involving umole
temp = model.getInitialAssignment('K_C00288bH')
formulaAST = temp.getMath()
formulastring = libsbml.formulaToString(formulaAST)
print formulastring
