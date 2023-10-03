
# Brute force optimization of cell volume
# Kwiseon Kim 031212
# rotation matrix with Euler angles, phi, theta, psi 
# orthorhombic (rectangluar) symmetry - 
#        restricts psi 0 to 90
#        perhaps there is further reduction but my head hurts now...
# full scan : phi, psi 0 to 360, theta 0 to 180
# VMD has it via
# transabout {0 0 1} phi
# transabout {1 0 0} theta
# transabout (0 0 1} psi

mol new hyde-pcenter.pdb
set OU [open "vmdvol.out" "a" ]

for {set phi 91} {$phi < 119} {incr phi 1} {
   set A [transabout {0 0 1} $phi deg ]
   for {set theta 16} {$theta < 29} {incr theta 1} {
      set B [transabout {1 0 0} $theta deg ]
      set BA [transmult $B $A]
      for {set psi 46} {$psi < 74} {incr psi 1} {
          set C [transabout {0 0 1} $psi deg ]
          set F [transmult $C $BA]
          set G [transtranspose $F]
#inverse of F
          
          [atomselect top all] move $F
          set P [measure minmax [atomselect top all]]
          set P0 [lindex  $P 0]
          set P1 [lindex  $P 1]
          set Q [vecsub  $P1  $P0]
          set V [expr [lindex  $Q 0] * [lindex  $Q 1] * [lindex  $Q 2]]
          puts  $OU  "$phi  $theta  $psi  $V"
# do the inverse and put back atoms in original position.
          [atomselect top all] move $G

     }
   }
}

close  $OU
exit
# After finished,
#   sort +3n vmdvol.out | head
#
#mol new hyde-pcenter.pdb
#[atomselect top all] move [transabout {0 0 1} xx deg ]
#[atomselect top all] move [transabout {1 0 0} yy deg]
#[atomselect top all] move [transabout {0 0 1} zz deg]
#measure minmax [atomselect top all]
#[atomselect top all] writepdb hyde-min.pdb
#exit
#


