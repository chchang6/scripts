package require psfgen

# STEP 1: Build Protein

# Script to split 1HFE into nine PDB files: one for each unique chain,
# one for H-cluster (including coupled [4Fe-4S]), and one for each [4Fe-4S] cluster.

# Load the PDB file
mol load pdb 1FEH+O2.pdb

# Set subsets
set chainH [atomselect top "chain A and not hetero"]
set clusterH [atomselect top "chain A and resid 580 581"]
set clusterA [atomselect top "chain A and resid 582"]
set clusterB [atomselect top "chain A and resid 583"]
set clusterC [atomselect top "chain A and resid 584"]
set cluster2 [atomselect top "chain A and resname F2O"]
set xtalwater [atomselect top "resname HOH"]
set oxygen [atomselect top "resname GAS"]

# Write these atoms to separate pdb files
$chainH writepdb built/chainH.pdb
$clusterH writepdb built/clusterH.pdb
$clusterA writepdb built/clusterA.pdb
$clusterB writepdb built/clusterB.pdb
$clusterC writepdb built/clusterC.pdb
$cluster2 writepdb built/cluster2.pdb
$xtalwater writepdb built/xtalwater.pdb
$oxygen writepdb built/oxygen.pdb
 
# Use the specified CHARMM27 topology file.
topology ../common/CHARMM_22prot_27lip.top
topology ../common/clusters_new.top

# Alias standard residues
pdbalias residue HIS HSD
pdbalias residue HOH TIP3
pdbalias atom HOH O OH2
pdbalias atom ILE CD1 CD

# Build nine segments, one for each chain or cluster
# Hydrogenase polypeptide
segment HYDR {
  first NTER
  last CTER
  pdb built/chainH.pdb
}

# H-cluster
segment HYDH {
  first NONE
  last NONE
  pdb built/clusterH.pdb
}

# proximal (bridged) cluster
segment HYDA {
  first NONE
  last NONE
  pdb built/clusterA.pdb
}

# medial cluster
segment HYDB {
  first NONE
  last NONE
  pdb built/clusterB.pdb
}

# distal cluster
segment HYDC {
  first NONE
  last NONE
  pdb built/clusterC.pdb
}

# 2Fe-2S cluster
segment HYDD {
  first NONE
  last NONE
  pdb built/cluster2.pdb
}

# Crystallographic water
segment XTAL {
  first NONE
  last NONE
  pdb built/xtalwater.pdb
}

# Gaseous dioxygen
segment OXY {
   first NONE
   last NONE
   pdb built/oxygen.pdb
}

# Patch to set up cluster ligation
patch F4-1O HYDH:581 HYDR:355
patch F4-2O HYDH:581 HYDR:499
patch F4-3O HYDH:581 HYDR:503
patch F4-4O HYDH:581 HYDR:300
patch HCB  HYDH:580 HYDR:503
patch F4-1O HYDA:582 HYDR:193
patch F4-2O HYDA:582 HYDR:157
patch F4-3O HYDA:582 HYDR:190
patch F4-4O HYDA:582 HYDR:196
patch F4-1O HYDB:583 HYDR:200
patch F4-2O HYDB:583 HYDR:150
patch F4-3O HYDB:583 HYDR:153
patch F4-4O HYDB:583 HYDR:147
patch FHO-1H HYDC:584 HYDR:94
patch FHO-2C HYDC:584 HYDR:107
patch FHO-3C HYDC:584 HYDR:98
patch FHO-4C HYDC:584 HYDR:101
patch F2-1O HYDD:585 HYDR:49
patch F2-1O HYDD:585 HYDR:62
patch F2-2O HYDD:585 HYDR:34
patch F2-2O HYDD:585 HYDR:46

# Load the coordinates for each segment.
coordpdb built/chainH.pdb HYDR
coordpdb built/clusterH.pdb HYDH
coordpdb built/clusterA.pdb HYDA
coordpdb built/clusterB.pdb HYDB
coordpdb built/clusterC.pdb HYDC
coordpdb built/cluster2.pdb HYDD
coordpdb built/xtalwater.pdb XTAL
coordpdb built/oxygen.pdb OXY

# Guess the positions of missing atoms.  As long as all the heavy
# atoms are present, psfgen usually does a very good job of this.
# However, the clusters will probably have very poor protonation.
# Edit these manually.

# Generate angles for clusters
regenerate angles

guesscoord
multiply 10 OXY:575

# Write output files
writepsf built/test.psf
writepdb built/test.pdb

