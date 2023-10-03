package require psfgen
package require solvate
package require autoionize

proc create_pdbs {} {
  mol new 1feh
  [atomselect top "resname HC1 and name O1 O4 O6"] set name {N1 N4 N6}
  [atomselect top "protein"] writepdb input/cp1-prot.pdb
  [atomselect top "not protein and not water and not (resname HC1 and name O2)"] writepdb input/cp1-metal.pdb
  [atomselect top "water"] writepdb input/cp1-wat.pdb 
}

proc create_crystal_structure {} {
  resetpsf
  topology /home/jordi/tools/topo/top_all27_prot_lipid.inp
  topology input/hyde.top

  pdbalias residue HIS HSD
  pdbalias atom ILE CD1 CD
  pdbalias residue HOH TIP3
  pdbalias atom HOH O OH2
  
  segment CP1 {
    pdb input/cp1-prot.pdb
    mutate 94 HSE
  }
  segment MTL {
    auto angles   ;# disable angle/dihedral autogeneration (?) 
    first none  ;# do not apply termini patches on non-protein residues
    last none
    pdb input/cp1-metal.pdb
  }
  segment XWT {auto none; pdb input/cp1-wat.pdb}
  
  coordpdb input/cp1-prot.pdb  CP1
  coordpdb input/cp1-metal.pdb MTL
  coordpdb input/cp1-wat.pdb   XWT


  patch FE1C MTL:581 CP1:355
  patch FE2C MTL:581 CP1:499
  patch FE3C MTL:581 CP1:503
  patch FE4C MTL:581 CP1:300

  patch FE1C MTL:582 CP1:193
  patch FE2C MTL:582 CP1:157
  patch FE3C MTL:582 CP1:190
  patch FE4C MTL:582 CP1:196
 
  patch FE1C MTL:583 CP1:200
  patch FE2C MTL:583 CP1:150
  patch FE3C MTL:583 CP1:153
  patch FE4C MTL:583 CP1:147


  patch FE1H MTL:584 CP1:94    ;#histidine
  patch FE2C MTL:584 CP1:107
  patch FE3C MTL:584 CP1:98
  patch FE4C MTL:584 CP1:101
  

  patch FE1C MTL:585 CP1:49
  patch FE1C MTL:585 CP1:62
  patch FE2C MTL:585 CP1:34
  patch FE2C MTL:585 CP1:46
  
  patch FE1C  MTL:580 CP1:503   ;# bind HC1 and Cys503 
  
 
  regenerate angles   ;# since my patches don't create angles
  
  guesscoord
  writepdb cp1-cryst.pdb
  writepsf cp1-cryst.psf
}

proc solvate_system {} {
   exec mkdir -p temp

  solvate cp1-cryst.psf cp1-cryst.pdb -o temp/cp1-solvated -s WT -minmax {{-25 50 25} {70 135 115}}
  
    autoionize -psf temp/cp1-solvated.psf -pdb temp/cp1-solvated.pdb -nna 15 -ncl 0 -o hyde


}



proc build_all {} {
  #create_pdbs
  create_crystal_structure
  solvate_system
}
