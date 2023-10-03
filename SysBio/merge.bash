sbtools merge -i -o TT C_rein_TCA_v2.3.xml C_rein_mitotrans_v2.3.xml
sbtools merge -i -o TTG TT C_rein_glycolysis_v2.3.xml
sbtools merge -i -o merge_TTGF.xml TTG C_rein_fermentation_v2.3.xml
#sbmltools merge -i -o TT C_rein_TCA_v2.3.xml C_rein_mitotrans_v2.3.xml
#sbmltools merge -i -o TTG TT C_rein_glycolysis_v2.3.xml
#sbmltools merge -i -o merge_TTGF.xml TTG C_rein_fermentation_v2.3.xml
rm TT TTG
