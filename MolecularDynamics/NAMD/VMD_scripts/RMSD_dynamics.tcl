lappend auto_path "/uhome/cchang/lib64/tcllib1.10"
package require math::statistics
# User settings
set num_frames 1000
set selection "all"
set PSFfilename nowaterions.psf
set DCDfilename 0-1.4ns.dcd
# Script--do not modify
set RMSD_list [list]
mol new $PSFfilename
mol addfile $DCDfilename
set reference [atomselect top $selection frame 0]
for {set frame 1} {$frame < $num_frames} {incr frame} {
   set target [atomselect top $selection frame $frame]
   set transformation_matrix [measure fit $target $reference]
   $target move $transformation_matrix
   lappend RMSD_list [measure rmsd $target $reference]
}
# Gather statistics on RMSDlist
set statsRMSD [math::statistics::basic-stats $RMSD_list]
puts -nonewline "Mean RMSD = "
puts [lindex $statsRMSD 0]
puts -nonewline "Minimum RMSD = "
puts [lindex $statsRMSD 1]
puts -nonewline "Maximum RMSD = "
puts [lindex $statsRMSD 2]
puts -nonewline "Sample variance = "
puts [lindex $statsRMSD 5]
puts -nonewline "Sample standard deviation ="
puts [lindex $statsRMSD 4]
