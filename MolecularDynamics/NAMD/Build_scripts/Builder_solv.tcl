package require psfgen

# Use the specified CHARMM27 topology file.
topology ../../common/CHARMM_22prot_27lip.top

mol load pdb input.pdb

# Water section for multiple water segments.
# Set limit of counter to number of water segments
for {set j 1} {$j <= 8} {incr j} {
   set water($j) [atomselect top "segname WT$j"]
   $water($j) writepdb built/${j}.pdb
   segment WT$j {
     first NONE
     last NONE
     pdb built/${j}.pdb
   }
   coordpdb built/${j}.pdb WT$j
}

# Now handle the ions
set ions [atomselect top "segname ION"]
$ions writepdb built/ions.pdb
segment ION {
  first NONE
  last NONE
  pdb built/ions.pdb
}
coordpdb built/ions.pdb ION

# Write output files
writepsf built/solvent.psf
writepdb built/solvent.pdb

