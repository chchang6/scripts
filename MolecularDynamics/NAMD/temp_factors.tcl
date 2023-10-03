mol new nowaterions.psf
mol addfile 0-1.0ns.dcd first 0 waitfor all
# Set global atom selection and those of interest for ANISOU information
set all_atoms [atomselect top all]
set selection_string "segname HYDA HYDH or (resid 355 300 499 503)"
set atoms_of_interest [atomselect top "$selection_string"]
set allframe0 [atomselect top all frame 0]
set partframe0 [atomselect top "$selection_string" frame 0]
# Create ANISO lists, one zero element per atom of interest.
$atoms_of_interest set beta 0
set U_xx_list [$atoms_of_interest get beta]
set U_yy_list [$atoms_of_interest get beta]
set U_zz_list [$atoms_of_interest get beta]
set U_xy_list [$atoms_of_interest get beta]
set U_xz_list [$atoms_of_interest get beta]
set U_yz_list [$atoms_of_interest get beta]
# Change frames 1-end of trajectory for maximum overlap of interesting atoms with frame 0.
set n [molinfo top get numframes]
$allframe0 moveby [vecinvert [measure center $partframe0]]
$allframe0 move [transaxis y 180]
$allframe0 move [transaxis z 90]
$allframe0 move [transaxis y -45]
$allframe0 move [transaxis x -10]
for {set i 1} {$i < $n} {incr i} {
   set x [measure fit [atomselect top "$selection_string" frame $i] $partframe0]
   [atomselect top all frame $i] move $x
}
# Calculate the average Cartesian position of each atom of interest.
set R_av [measure avpos $atoms_of_interest first 0 last [expr $n - 1]]
# Loop over the trajectory again. For each atom at each frame, calculate the deviation from the average.
# Then, add U_ij to the running totals for each atom. This is why the zero lists were created above.
for {set i 0} {$i < $n} {incr i} {
   set fluc_vecs [list]
   foreach j $R_av k [[atomselect top "$selection_string" frame $i] get {x y z} ] {
      lappend fluc_vecs [vecsub $k $j]
   }
   for {set j 0} {$j < [llength $fluc_vecs]} {incr j} {
      lset U_xx_list $j [expr [lindex $U_xx_list $j] + pow([lindex [lindex $fluc_vecs $j] 0],2)]
      lset U_yy_list $j [expr [lindex $U_yy_list $j] + pow([lindex [lindex $fluc_vecs $j] 1],2)]
      lset U_zz_list $j [expr [lindex $U_zz_list $j] + pow([lindex [lindex $fluc_vecs $j] 2],2)]
      lset U_xy_list $j [expr [lindex $U_xy_list $j] + [lindex $fluc_vecs $j 0]*[lindex $fluc_vecs $j 1]]
      lset U_xz_list $j [expr [lindex $U_xz_list $j] + [lindex $fluc_vecs $j 0]*[lindex $fluc_vecs $j 2]]
      lset U_yz_list $j [expr [lindex $U_yz_list $j] + [lindex $fluc_vecs $j 1]*[lindex $fluc_vecs $j 2]]
   }
   unset fluc_vecs
}
unset R_av
# Calculate isotropic B factors and set beta values
set B_list [list]
foreach i $U_xx_list j $U_yy_list k $U_zz_list {
   lappend B_list [expr ($i + $j + $k)/($n-1) * 8 * pow($M_PI,2) / 3]
}
foreach atom [$atoms_of_interest get index] B $B_list {
   [atomselect top "index $atom"] set beta $B
}
$atoms_of_interest writepdb test.pdb
# Now, divide through lists by 1/(number of frames - 1) and output to file
set outlist [list]
foreach i [$atoms_of_interest get name] j $U_xx_list k $U_yy_list l $U_zz_list m $U_xy_list o $U_xz_list p $U_yz_list {
   lappend outlist [list $i [expr int($j/($n-1)*1e4)] [expr int($k/($n-1)*1e4)] [expr int($l/($n-1)*1e4)] [expr int($m/($n-1)*1e4)] [expr int($o/($n-1)*1e4)] [expr int($p/($n-1)*1e4)]]
}
set outfile [open aniso.log w]
foreach i $outlist j [$atoms_of_interest get resname] k [$atoms_of_interest get resid] l [$atoms_of_interest get serial] m [$atoms_of_interest get element] {
   puts $outfile [format "ANISOU%5i  %-3s %3s  %4i  %7i%7i%7i%7i%7i%7i      %2s" $l [lindex $i 0] $j $k [lindex $i 1] [lindex $i 2] [lindex $i 3] [lindex $i 4] [lindex $i 5] [lindex $i 6] $m]
}
close $outfile
