package provide pathways 0.1

namespace eval pathways {
   variable w			# Main window
   variable active_molid	# Active molecule id number
   variable ti_threshold        # Transfer integral value at which to terminate searches for pathways
   variable hbonddist_value     # Maximum distance between two atoms that could be hydrogen-bonded
   variable hbondangle_value    # Minimum angle at which X, H, and Y could form X-H-Y hydrogen bond
   variable tsdist_value        # Maximum spherical radius from donor in which to consider acceptor atoms
}

proc pathways::init {} {
   variable w
   set w [toplevel .pathways -width 50 -height 100]
   wm title $w "VMD Pathways Analyzer"
   wm resizable $w 0 0
# Get id number of active molecule
   foreach x1 [molinfo list] {
      set x2 [molinfo $x1 get active]
      if { $x2 == 1 } {
         set active_molid $x1
      }
   }
# Set up master container
   frame $w.main

# Set up top row with molecule name displayed, and donor/acceptor
#   input boxes, packed into frames for inclusion into master grid.
   label $w.molid -text "Molecule: [molinfo $active_molid get name]"

#   Donor information
   frame $w.donorframe
   label $w.donorframe.label -text "Donor atom index: "
   entry $w.donorframe.box -width 7 -textvariable donor_index -state normal
   pack $w.donorframe.label $w.donorframe.box -side left -in $w.donorframe

#   Acceptor information
   frame $w.acceptorframe
   label $w.acceptorframe.label -text "Acceptor atom index: "
   entry $w.acceptorframe.box -width 7 -textvariable acceptor_index -state normal
   pack $w.acceptorframe.label $w.acceptorframe.box -side left -in $w.acceptorframe

# Set up the standard out scrollable text box
   frame $w.stdout
   text $w.stdout.box -width 30 -height 30 -xscrollcommand "$w.stdout.xscrl set" -yscrollcommand "$w.stdout.yscrl set"
   scrollbar $w.stdout.xscrl -command "$w.stdout xview" -orient h
   scrollbar $w.stdout.yscrl -command "$w.stdout yview" -orient v
   grid $w.stdout.box -row 1 -column 1 -in $w.stdout
   grid $w.stdout.xscrl -row 2 -column 1 -in $w.stdout -sticky ew
   grid $w.stdout.yscrl -row 1 -column 2 -in $w.stdout -sticky ns
   pack $w.stdout

# Initialize variables to default values
   set ti_threshold 0.01
   set hbond_dist 3.5
   set hbond_angle 150
   set ts_threshold 4.0

# Declare threshold input boxes and action buttons
   label $w.threshold_label -text "Transfer integral threshold\nDefault 0.010"
   label $w.hbonddist_label -text "H-bond distance threshold\nDefault 3.5"
   label $w.hbondangle_label -text "H-bond angle threshold\nDefault 150"
   label $w.tsdist_label -text "Max through-space transfer step\nDefault 4.0"
   scale $w.threshold_value -resolution 0.005 -length 150 -digits 2 -from 0.000 \
     -to 0.050 -tickinterval 0.025 -variable ti_threshold -orient h
   scale $w.hbonddist_value -resolution 0.1 -length 150 -digits 2 -from 2.5 -to 4.0 \
     -tickinterval 0.5 -variable hbond_dist -orient h
   scale $w.hbondangle_value -resolution 1 -length 150 -digits 3 -from 130 -to 170 \
     -tickinterval 10 -variable hbond_angle -orient h
   scale $w.tsdist_value -resolution 0.1 -length 150 -digits 3 -from 4.0 -to 10.0 \
     -tickinterval 1 -variable ts_threshold -orient h
   button $w.go -text "Calculate!" -command "pathways **donor** **acceptor** $ti_threshold $hbond_dist $hbond_angle $ts_threshold"
   button $w.save -text "Save to file..." -command "tk_getSaveFile -defaultextension pth -filetypes {.pth}"
   set numpaths 10

# Lay master grid out
   grid $w.molid -row 1 -column 1 -in $w.main
   grid $w.donorframe -row 1 -column 2 -in $w.main
   grid $w.acceptorframe -row 1 -column 3 -in $w.main
   grid $w.stdout -in $w.main -row 2 -column 1 -rowspan 6
   grid $w.threshold_label -in $w.main -row 2 -column 2
   grid $w.hbonddist_label -in $w.main -row 3 -column 2
   grid $w.hbondangle_label -in $w.main -row 4 -column 2
   grid $w.tsdist_label -in $w.main -row 5 -column 2
   grid $w.go -in $w.main -row 6 -column 2
   grid $w.threshold_value -in $w.main -row 2 -column 3
   grid $w.hbonddist_value -in $w.main -row 3 -column 3
   grid $w.hbondangle_value -in $w.main -row 4 -column 3
   grid $w.tsdist_value -in $w.main -row 5 -column 3
   grid $w.save -in $w.main -row 6 -column 3

# Combine # pathways to display and string "Pathways" into 1 widget
# and place it in the layout
   frame $w.gen1
   button $w.display -text "Display" -command "**proc pathways_display**"
   entry $w.gen1.numdisplay -width 7 -textvariable numpaths -state normal
   label $w.gen1.label -text "Pathways"
   pack $w.display $w.gen1.numdisplay $w.gen1.label -in $w.gen1 -side left
   grid $w.gen1 -in $w.main -row 7 -column 2 -columnspan 2

# Pack it!
   pack $w.main
}
   
proc pathways_tk {} {
    ::pathways::init
    return $pathways::w
}

proc pathways_display {} {
}
