# visual_hbonds - Dynamic Visualization of H-bonds calculated with MDEnergy
# -------------------------------------------------------------------------

# Shows each H-bond as a cylinder whose thickness scales with the H-bond 
# energy as computed by MDEnergy. Using MDEnergy with the options -hbond 
# -hpar <H-bond-parameterfile> -hb <energyoutputfile> to generate a file 
# containing the indices of all atoms involved in an Hbond and their energies
# for every frame. This file is read by visual_hbonds and each time a new frame
# is displayed the new H-bonds are drawn. You will see them varying according
# to the bond distance and angle. I found this very ilustrative.

# Usage:
# visual_hbonds $energyfile [$molid] [$color]

# Other functions:
# hbcolor $colorname     - Change H-bond color
# hbresolution $res      - Change resolution of the drawn cylinders
# hbscale $min $max $fac - Change the min/max energies for which hbonds 
#                          are displayed and the thickness scaling factor
# hbdisconnect - delete the trace that was set on vmd_frame to update the 
#                hbonds. If you don't delete the old trace before loading a new 
#                set of hbonds then VMD has to redraw the Bonds always twice.
#                In a later version this should be done automatically...

# Example:
# source ~/vmd/tcl/hbonds.tcl
# visual_hbonds /Projects/saam/mdnergy/src/hbfile 0
# hbscale 0.01 3.0  2
# hbcolor yellow
# hbdisconnect

namespace eval ::HBonds:: {
  namespace export visual_hbonds update_frame 
 
   variable molid [molinfo top get id]
   variable graphics_id;      
   variable energy_list;      # H-bond energies from MDEnergy
   variable numHbonds  0;     # numberof H-bonds for each frame
   variable sel;              # the atomselection
   variable Emin       0.1;   # min energy for H-bond to be displayed
   variable Emax       5.0;   # upper limit for thickness scaling
   variable scale      1;     # thickness scaling factor
   variable color      green; # color of the H-bonds
   variable resolution 6;     # resolution of the drawn cylinders
}

# Just a wrapper to be able to omit the "::HBonds::" prefix
proc visual_hbonds { args } {::HBonds::visual_hbonds $args }

proc ::HBonds::visual_hbonds { filename {usermolid top} {usercolor green}} {
   global vmd_frame
   variable energy_list
   variable numHbonds
   variable molid
   variable graphics_id
   variable sel
   variable Emin
   variable Emax
   variable scale
   variable color
   variable resolution
   set color $usercolor
   set molid [molinfo $usermolid get id]
   set fd [open $filename r]
   set nframes 0

   # Read header
   set natoms  [gets $fd]
   set seltext [gets $fd]
   #mol load graphics HBonds
   
   puts "current frame : $vmd_frame($molid)"
   puts "natoms        : $natoms"
   puts "selection text: $seltext"
   puts "min energy for scaling: $Emin"
   puts "max energy for scaling: $Emax"
   

   set sel [atomselect $molid "$seltext"]
   
   # Read the betalist
   set energy_list ""
   while {![eof $fd]} {
      set frame [gets $fd]  
      set nHbonds [gets $fd]
      set HBenergy [gets $fd]
      if {[llength $frame]>0} {
	 if {! [expr $frame%10]} {puts "initializing frame $frame"}
	 lappend numHbonds $nHbonds
	 lappend energy_list $HBenergy 
	 incr nframes
      }
   }
   puts "Finished. Read $nframes frames."
   #set graphics_id [molinfo top]
   
   ::HBonds::update_frame
   
   # Define callback to update the frames
   trace add variable vmd_frame($::HBonds::molid) write ::HBonds::update_frame 

}


# This function is called whenever a new frame is displayed
proc ::HBonds::update_frame { args } {
   global vmd_frame
   variable energy_list
   variable molid
   variable color
   variable Emin
   variable Emax
   variable scale
   variable resolution
   
   draw delete all
   draw color $color
   set hbondlist [lindex $energy_list $vmd_frame($molid)]
   
   foreach {c1 c2 E} $hbondlist {
      if {$E>$Emin} then {
	 if {$E>$Emax} then {set E $Emax}
	 set rad [expr $E*$scale*0.2]
	 draw cylinder $c1 $c2 radius $rad resolution $resolution
      }
   }
}


# Disconnect the trace on vmd_frame
proc hbdisconnect {} {
   global vmd_frame

   trace remove variable vmd_frame($::HBonds::molid) write ::HBonds::update_frame
   
   # Check for hanging traces:
   set traces [trace info variable vmd_frame($::HBonds::molid)]
   if {[llength $traces] > 0} {
      puts "[llength $traces] remaining traces on vmd_frame($::HBonds::molid):"
      puts $traces
   }
   
   # Reset some values:
   set ::HBonds::Emin 0.1
   set ::HBonds::Emax 5.0
   set ::HBonds::scale 1
   #mol delete $::HBonds::graphics_id
   draw delete all
}


proc ::HBonds::drawhbond {c1 c2 E {res 6}} {
   variable molid
   puts "$c1 $c2 $E"
   draw cylinder $c1 $c2 radius $E resolution $res
}

# Change H-bond color
proc hbcolor {text} {
    set ::HBonds::color $text
    ::HBonds::update_frame
}

# Change resolution of the drawn cylinders
proc hbresolution {res} {
    set ::HBonds::resolution $res
    ::HBonds::update_frame
}

# Change the min/max energies for which hbonds are displayed and the 
# thickness scaling factor
proc hbscale {lo hi scale} {
    set ::HBonds::Emin $lo
    set ::HBonds::Emax $hi
    set ::HBonds::scale $scale
    ::HBonds::update_frame
} 
