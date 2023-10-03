package require Tclx

# lempty A returns 0 if list A is not empty.
# llength A returns length of list A
# lsearch A B returns the index of item in list A matching pattern B
# lvarpop A B removes item index B from list A
# lvarpush A B C inserts B into list A before index C
# lindex A B gets Bth indexed item of list A
# lcontain A B returns true if B is in A, otherwise false

proc process x {
   global donor_index
   global acceptor_index
   # x is a pathways, i.e., a two-element list: an ordered list of atom indices, and a cumulative transfer integral
   # Find all atoms within a user-specified radius of the last element in the atomselection list.
   set atomlist [lindex $x 0]
   set coupling [lindex $x 1]
   # Set probe_index to the index value of probe
   set probe_index [lindex $atomlist [expr [llength $atomlist] - 1 ]]
   # Probe is the last atom in the pathway. Set probe to VMD atom selection of 1 atom.
   set probe [atomselect top "index $probe_index"]
   # Create list of bonds to probe
   set probe_bonds_list [$probe getbonds]
   # Create test_index_list of list-of-candidate-indices-next-in-pathway
   set test_index_list [[atomselect top "within 4 of index $probe_index"] list]
   # Eliminate atoms from test already in atomlist (e.g., probe)
   # Eliminate from remaining atoms any that lead away from the acceptor
   foreach i $test_index_list {
      if { [lcontain $atomlist $i] } {
         lvarpop test_index_list [lsearch $test_index_list $i]
      }
   }
   # Each of the atoms indexed in test_index_list will form a new Pathway. Need to figure out what
   # type of interaction exists between the last element of $x[0] (terminal atom input
   # into this routine) and each test_index_list atom. Create new list final_process_list containing index and
   # cumulative transfer integral value.
   foreach i $test_index_list {
      lvarpush atomlist $i len
      set probe_i_distance [measure bond [list $probe_index $i ]]
      # If there is a bond to probe, scale cumulative coupling by 0.6
      if {[lcontain $probe_bonds_list $i]} {
         lappend final_process_list [list $atomlist [expr $coupling * 0.6]]
      # Else if there is a hydrogen bond, scale by 0.36 * exp of distance
      } elseif {[lempty [lindex [measure hbonds 3.5 150.0 $probe [atomselect top "index $i"]] 0 ]] == 0} {
         lappend final_process_list [list $atomlist [expr $coupling * 0.36 * exp($probe_i_distance - 2.8)]]
      # Otherwise there must only be a through-space coupling
      } else {
         lappend final_process_list [list $atomlist [expr $coupling * 0.6 * exp(-1.7 * ($probe_i_distance - 1.4))]]
      }
      lvarpop atomlist end
   }
   return $final_process_list
}

# "trim" iterates through working_list, and doing one of three things:
# 1) If Pathway has not reached the acceptor and has a cumulative transfer integral
#    value below the threshold, deletes the Pathway from further consideration;
# 2) If the Pathway has reached the acceptor, moves it to global list "Pathways_list";
# 3) If Pathway has not reached the acceptor and has a cumulative transfer integral
#    value above the threshold, does nothing;
# "trim" intended to accept "working_list" as input.

proc trim x {
   global acceptor_index
   global Pathways_list
   global transfer_integral_threshold
   for {set i 0} {$i < [llength $x]} {incr i} {
      set atomlist [lindex [lindex $x $i] 0]
      set coupling [lindex [lindex $x $i] 1]
      if {$coupling < $transfer_integral_threshold} {
#         puts -nonewline "POPPED "
         lvarpop x $i
         set i [expr $i - 1]
      } elseif {[lcontain $atomlist $acceptor_index]} {
         lappend Pathways_list [lvarpop x $i]
         set i [expr $i - 1]
      } else {
         continue
      }
   }
   return $x
}

# Preliminaries: load molecule, set donor and acceptor atoms.
set frame [lindex $argv 0]
mol new 0-2.0ns.dcd type dcd first $frame last $frame waitfor all
mol addfile nowaterions.psf
set transfer_integral_threshold 2e-3
set donor [atomselect top "index 3043"]
set acceptor [atomselect top "index 2411"]
set donor_index [$donor list]
set acceptor_index [$acceptor list]

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
# Calculate the coupling value by multiplying the old value by the value for the appropriate
# interaction type. Test the coupling; if it falls below the threshold (to be given by user
# through graphical interface), remove the entry from the list.
#
# Continue until the acceptor is reached; once it is, move that Pathway to a collection list.
# Once the analysis is done, the user should be able to plot all Pathways with integrals above
# a defined value onto the structure.
# working_list is a list-of-pathways; a pathway is a list of [list-of-atoms, coupling]. A list-of-atoms is [atom_index11, atom_index2,...]

set working_list [list [list [list $donor_index] 1.0]]
set Pathways_list {}
set cycle 0
while { [lempty $working_list] == 0 } {
   incr cycle
#   puts -nonewline "Cycle "
#   puts -nonewline $cycle
#   puts -nonewline " frame "
#   puts -nonewline $frame
#   puts -nonewline " Pathways list "
#   puts $Pathways_list
   foreach i $working_list {
      set temp [process [lvarpop working_list [lsearch $working_list $i]]]
      foreach j $temp {
         lappend working_list2 $j
      }
   }
   set working_list $working_list2
   unset working_list2
   set working_list [trim $working_list]
}
puts -nonewline "Pathways list for frame "
puts -nonewline $frame
puts -nonewline " is: "
puts $Pathways_list
