package require psfgen

# Use the specified CHARMM27 topology file.
topology ./common/terminal_methyl.top
topology ./common/Crclusters_new2.top

# Load the PDB file
mol load pdb H-cluster8.pdb

# Set subsets
set ligands [atomselect top "chain A and resname CYS"]
set clusterH [atomselect top "chain A and resid 580"]
set clusterF [atomselect top "chain A and resid 581"]

# Write these atoms to separate pdb files
$ligands writepdb built/ligands.pdb
$clusterH writepdb built/clusterH.pdb
$clusterF writepdb built/clusterF.pdb
 
# Build nine segments, one for each chain or cluster
# Hydrogenase polypeptide
segment LGND {
  first NONE
  last NONE
  pdb built/ligands.pdb
}

# H-cluster
segment HYDH {
  first NONE
  last NONE
  pdb built/clusterH.pdb
}

# proximal (bridged) cluster
segment HYDF {
  first NONE
  last NONE
  pdb built/clusterF.pdb
}

# Patch to set up cluster ligation
patch F4-1O HYDF:581 LGND:355
patch F4-2O HYDF:581 LGND:499
patch F4-3O HYDF:581 LGND:503
patch F4-4O HYDF:581 LGND:300
patch HCB  HYDH:580 LGND:503

# Load the coordinates for each segment.
coordpdb built/ligands.pdb LGND
coordpdb built/clusterH.pdb HYDH
coordpdb built/clusterF.pdb HYDF

# Guess the positions of missing atoms.  As long as all the heavy
# atoms are present, psfgen usually does a very good job of this.

guesscoord

# Write output files
writepsf built/test.psf
writepdb built/test.pdb

