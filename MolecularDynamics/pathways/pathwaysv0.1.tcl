package require Tclx

proc process x {
   puts "process"
   global donor_index
   global acceptor_index
   # x is a two-element list: an ordered list of atom indices, and a cumulative transfer integral
   # Find all atoms within a user-specified radius of the last element in the atomselection list.
   set atomlist [lindex $x 0]
   set float [lindex $x 1]
#   puts -nonewline "x: "
#   puts $x
#   puts -nonewline "atomlist: "
#   puts $atomlist
   set probe [atomselect top "index [lindex $atomlist [expr [llength $atomlist] - 1 ]]"]
   set probe_index [lindex $atomlist [expr [llength $atomlist] - 1 ]]
#   puts -nonewline "probe_index: "
#   puts $probe_index
   set probe_bonds_list [$probe getbonds]
   set test_index_list [[atomselect top "within 4 of index $probe_index"] list]
#   puts -nonewline "test_index_list: "
#   puts $test_index_list
   # Eliminate atoms from test already in atomlist (e.g., probe)
   # Eliminate from remaining atoms any that lead away from the acceptor
   foreach i $test_index_list {
      if { [lcontain $atomlist $i] } {
         lvarpop test_index_list [lsearch $test_index_list $i]
#         puts -nonewline "POPPED index "
#         puts $i
      }
#       else {   set angle [measure angle [list $probe_index $i $acceptor_index ]]
#         if {$angle < 90} {
#            lvarpop test_index_list [lsearch $test_index_list $i]
#            puts -nonewline "POPPED index "
#            puts $i
#         }
#      }
   }
#   puts -nonewline "test_index_list after filtering: "
#   puts $test_index_list
   # Each of the atoms indexed in test_index_list will form a new Pathway. Need to figure out what
   # type of interaction exists between the last element of $x[0] (terminal atom input
   # into this routine) and each test_index_list atom. Create new list final_process_list containing index and
   # tag: "C" for covalent, "H" for hydrogen-bond, and "S" for through-space.
   set final_process_list {}
   foreach i $test_index_list {
      lvarpush atomlist $i len
#      puts -nonewline "process: Atomlist after push: "
#      puts $atomlist
      set probe_i_distance [measure bond [list $probe_index $i ]]
      if {[lcontain $probe_bonds_list $i]} {
         lappend final_process_list [list $atomlist [expr $float * 0.6]]
      } elseif {[hydrogen_bonds $probe_index $i] == 1} {
         lappend final_process_list [list $atomlist [expr $float * 0.36 * exp($probe_i_distance - 2.8)]]
      } else {
         lappend final_process_list [list $atomlist [expr $float * 0.6 * exp(-1.7 * ($probe_i_distance - 1.4))]]
      }
      lvarpop atomlist end
#      puts -nonewline "process: Atomlist after pop: "
#      puts $atomlist
   }
   return $final_process_list
}

proc hydrogen_bonds {x i} {
#   puts "hydrogen_bonds"
   global polarH_indices
   # Find if there is a hydrogen bond between atoms with indices x and i
   set distance_threshold 3.0
   set angle_threshold 60
   set donor_types [list "NR1" "NR3" "NH1" "NH2" "NH3" "NC2" "NY" "NP" "OC" "OH1" "OT" "OS"]
   set acceptor_types [list "N" "NR2" "O" "OC" "OH1" "OS" "OT" "S"]
   set xtype [[atomselect top "index $x"] get type]
   set itype [[atomselect top "index $i"] get type]
   set truth 1
   # Now test for two alternative scenarios:
   # 1) x is a hydrogen-bond donor, has an attached polarH, and i is a hydrogen-bond acceptor, or
   # 2) x is a hydrogen-bond acceptor, i is a hydrogen-bond donor, and has an attached polarH
   # First, try ruling out either based on x and i types
   set test1 [lcontain $donor_types $xtype]
   set test2 [lcontain $donor_types $itype]
   set test3 [lcontain $acceptor_types $xtype]
   set test4 [lcontain $acceptor_types $itype]
   if { [expr $test1 + $test2] == 0 || [expr $test3 + $test4] == 0 } {
      set truth 0
   } else {
   # The types are right; see if the donor has a polar hydrogen attached and in the right geometry.
      set bondlength [measure bond [ list $x $i ]]
      if {[lcontain $donor_types $xtype]} {
         set temp [[atomselect top "index $x"] getbonds]
         set temp2 [intersect $temp $polarH_indices]
         if { [lempty $temp2] == 0 } {
            if {[measure angle [list $x $temp2 $i ]] < $angle_threshold &&
                $bondlength < $distance_threshold } {
               # Leave $truth as 1
            } else {
               set truth 0
            }
         }
      } else {
      # x is an acceptor
         set temp [[atomselect top "index $i"] getbonds]
         set temp2 [intersect $temp $polarH_indices]
         if { [lempty $temp2] == 0 } {
            if {[measure angle [list $x $temp2 $i ]] < $angle_threshold &&
                $bondlength < $distance_threshold} {
               # Leave $truth as 1
            } else {
               set truth 0
            }
         }
      }
   }
   return $truth
}

# "trim" iterates through working_list, and doing one of three things:
# 1) If Pathway has not reached the acceptor and has a cumulative transfer integral
#    value above the threshold, does nothing;
# 2) If Pathway has not reached the acceptor and has a cumulative transfer integral
#    value below the threshold, deletes the Pathway from further consideration;
# 3) If the Pathway has reached the acceptor, moves it to global list "Pathways_list".
# "trim" intended to accept "working_list" as input.

proc trim x {
   puts -nonewline "trim x = "
   puts $x
#   puts -nonewline "first element of trim x = "
#   puts [lindex $x 0]
#   puts -nonewline "first element of first element of x = "
#   puts [lindex [lindex $x 0] 0]
   global acceptor_index
   global Pathways_list
   global transfer_integral_threshold
   for {set i 0} {$i < [llength $x]} {incr i} {
      set atomlist [lindex [lindex $x $i] 0]
#      puts -nonewline "trim atomlist = "
#      puts $atomlist
      set float [lindex [lindex $x $i] 1]
#      puts -nonewline "trim float = "
#      puts $float
      if {[lcontain $atomlist $acceptor_index]} {
         puts -nonewline "PATHWAY: "
         puts $atomlist
         lappend [lvarpop x $i] Pathways_list
         set i [expr $i - 1]
      } elseif {$float < $transfer_integral_threshold} {
#         puts $float
#         puts -nonewline "POPPED "
#         puts [lvarpop x $i]
#         puts -nonewline "x is now "
#         puts $x
         set i [expr $i - 1]
      } else {
         continue
      }
   }
   return $x
}

# Preliminaries: load molecule, set donor and acceptor atoms, and create list of polar hydrogen indices.
mol new dyn_2.0ns_out.coor
mol addfile 1FEH_OOOOOO.psf
set transfer_integral_threshold 1e-6
set donor [atomselect top "index 3043"]
set acceptor [atomselect top "index 2411"]
set donor_index [$donor list]
set acceptor_index [$acceptor list]
# Create reference list of polar hydrogen indices
set polarH_types [list "H" "HC" "HT" "HS"]
set polarH_indices {}
foreach i [[atomselect top "not water"] list] {
   set temp [[atomselect top "index $i"] get type]
   if {[lcontain $polarH_types $temp]} {
      lappend polarH_indices $i
   }
}

# Code to carry out Pathways analysis as described in Science 282: 1285-8 (1991).
# Build a list of lists, each with two components: a list of atom indices, and a float.
# The atom index list is an ordered Pathway; the float is the cumulative transfer integral
# value.
#
# For each "terminal" atom in an atomselection list, create a list of "next atoms"
# within direct transfer distance and with the angle between the terminal atom-acceptor
# vector and the terminal atom-next atom vector less than 90 degrees.
#
# For each interaction, determine if it's covalently bonded, hydrogen bonded, or through-space.
# Then create new lists, each with the present Pathway and appending the next atom.
#
# Calculate the float value by multiplying the old value by the value for the appropriate
# interaction type. Test the float; if it falls below the threshold (to be given by user
# through graphical interface), remove the entry from the list.
#
# Continue until the acceptor is reached; once it is, move that Pathway to a collection list.
# Once the analysis is done, the user should be able to plot all Pathways with integrals above
# a defined value onto the structure.
set working_list [list [list [list $donor_index] 1.0]]
#puts -nonewline "First element of working_list before main: "
#puts [lindex $working_list 0]
#puts -nonewline "First element of first element of working_list before main: "
#puts [lindex [lindex $working_list 0] 0]
set Pathways_list {}
set j 0
while { [lempty $working_list] == 0 } {
   incr j
   puts -nonewline "main beginning. Cycle: "
   puts $j
   for {set i 0} {$i < [llength $working_list]} {incr i} {
#      puts -nonewline "Passing this to process: "
#      puts [lindex $working_list $i]
      set temp [process [lindex $working_list $i]]
#      puts -nonewline "Got back from process: "
#      puts $temp
#      puts -nonewline "working_list before replace: "
#      puts $working_list
#      puts -nonewline "First element of working_list before replace: "
#      puts [lindex $working_list 0]
      set working_list [lreplace $working_list $i $i [lrange $temp 0 end] ]
#      puts -nonewline "working_list after replace:"
#      puts $working_list
   }
#   puts -nonewline "First element of working_list before trim: "
#   puts [lindex $working_list 0]
#   puts -nonewline "Second element of working_list before trim: "
#   puts [lindex $working_list 1]
#   puts -nonewline "First element of first element of working_list before trim: "
#   puts [lindex [lindex $working_list 0] 0]
   set working_list [trim $working_list 0]
#   puts -nonewline "main end. Value of lempty working_list: "
#   puts [lempty $working_list]
}
puts -nonewline "Pathways list is: "
puts $Pathways_list
