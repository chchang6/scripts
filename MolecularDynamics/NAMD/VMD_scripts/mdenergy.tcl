# mdenergy --- by Jan Saam, 01/09/2003
# saam@charite.de

# This script is a tool to compute energies conveniently in VMD.

# It computes the energy for a selection or the interaction energy between 
# two selections using the C++ program 'MDEnergy' which was derived from NAMD.

# MDEnergy is basically a single processor version of the NAMD engine which 
# allows the command line driven output of bonded and nonbonded energies per 
# atom for each frame of a dcd file. It loads only one frame at a time thus 
# it doesn't consume a lot of memory.

# The procedure 'mdenergy' calls the C++ program MDEnergy. Binaries can be build
# for Linux, Solaris and Irix, but it should be possible to compile it on other 
# systems, too. The script tries to determine which binary to run.
# If the machine architecture cannot be auto determined correctly set the
# variable MDENERGY in this script manually to your appropriate binary.

# Unless you specified the option -visual MDEnergy runs as a background process 
# so you can continue your work in VMD.
# The output is similar to NAMD's output and you can plot it with 'namdplot'
# (a tool which is part of the NAMD distribution). When you 

# Any errors in the execution of MDEnergy but also successful starting and 
# finishing are reported in the VMD console.

# Usage: 
# energy -bond|-angle|-dihed|-impr|-vdw|-elec|-nonb|-all|-hbon -sel $sel [$sel2] [options]

# You must specify one or more of the following keywords to tell 
# energy/mdenergy which energies it has to calculate:
# -all       - All energies are computed (except kinetic energy)
# -bond      - bond energy
# -angl      - angle energy
# -dihe      - dihedral energy
# -impr      - improper energy
# -vdw       - van der Waals energy
# -elec      - electrostatic energy
# -nonb      - nonbonded energies (elec+vdw)
# -conf      - conformational energy (bond+angl+dihe+impr)
# -kin       - kinetic energy (must also specify -veldcd)
# -hbon      - Computes h-bond energies (angle and distance dependent)
#              which can be very nicely visualized in VMD with the script
#              visual_hbonds (in 'hbonds.tcl'). See documentation therein.
#              If you also specify -visual this is done automatically.
#              You need to have:
#              A psf file with populated NBON and NACC fields to tell
#              MDEnergy about the donors and acceptors in your system.
#              You can generate it using the 'hbondpsf' tool which is
#              contained in this distribution. With the help of the 
#              DONOR/ACCEPTOR information in the topology file and an
#              existing psf file it generates a new psf including the
#              required donor/acceptor info.
#              -hpar file : h-bond parameter file
#                           A sample file that should be sufficient for
#                           most cases is provided in hbonds/hpar
#              Optional:
#              -pat file  : If there are patches in the molecule, then
#                           specify them in a file in th same format as
#                           you would do for 'psfgen'. If you wish to 
#                           consider C- and N-terminus you have to define 
#                           them as an explicit patch, too.
 

# You MUST also specify at least one selection that you generated with VMD
# using "-sel $sel". If you specify a second selection "-sel $sel $sel2"
# then the interaction energy between these two groups of atoms is computed.

# Options: (defaults)
# -------------------
# -ofile  - redirect the output into this file  otherwise it's written to
#           the VMD console (/dev/tty).
# -afile  - write energies for all atoms into this file. (none)
#	    This file can be used by 'viz_energy filename' to visualize 
#	    the energies.

# -beg    - start with this frame    (current frame)
# -end    - end with this frame      (current frame)
#           you can use 'end last' to specify the last frame. 

# -par    - charmm parameter file. Only one can be specified, it must
#           contain parametersfor all atoms in the molecule.
#           Change the default
#           (/projects/namd/toppar/par_all27_prot_lipid_ret.inp)
#           to your favorite file.

# -xplor  - xplor parameter file
#           (default is the charmm file)

# -avg     - sliding window average width (0, no average computed) 
# -avgmode - (ramp/pad) To preserve frame number the average is ramped 
#            up and down or the averaged trajectory is padded with the 
#            first and last frame to get the right frame number.
#            (the default set to nothing)

# -switch - switch distance for electrostatic interactions (10)
# -cutoff - cutoff distance (12)

# -self   - the nonbonded interactions is computed only within the selection.
#           Otherwise the interaction of the selection with the environment is
#           included. Does not apply if you specified two selections.

# -vel    - Specify the velocity DCD file which is needed for the -kin option. (none)

# -visual - Vizualizes the atom based energy values using the script visual_mdenergy.tcl
#           The atom energies are dumped by mdenergy into a file (option -a <filename>)
#           This file is then read by visual_energy and the atom anergies are filled 
#           into the user data field in VMD and colored according to this value. 
#           By default VMD uses the min/max values of the current frame to set the 
#           color scale, here we use the min/max over all frames of the trajectory.
#           You can change the color scaling in the Graphics->Color menu or using
#           mol scaleminmax molecule_number rep_number [min max | auto]
#           If you didn't specify a filename by -a <file> then the default filename 
#           "energy_per_atom.dat" is chosen.



# Example:
# source ~/vmd/tcl/mdenergy.tcl
# set sel1 [atomselect top "resname ALA"]
# mdenergy -vdw -sel $sel1 -ofile "out.dat" -beg 0 -end last -switch 11 -cutoff 13 -self


proc mdenergy { args } {
   global MDENERGY_PID
   if {[lindex $args 0]=="stop"} {
      enstop
      return 
   }

   # If the machine architecture cannot be auto determined set MDENERGY and 
   # HBONDPSF manually to your appropriate binaries.
   set  MDENERGY mdenergy.[get_machine_arch]
   set  HBONDPSF hbondpsf.[get_machine_arch]

   # Directory containing the binaries
   set MDE_PATH /usr/local/bin

   # Full path of the binaries:
   set MDE_RUN "$MDE_PATH/$MDENERGY"
   set HBP_RUN "$MDE_PATH/$HBONDPSF"
   
   set defpar "/projects/namd/toppar/par_all27_prot_lipid_ret.inp"
   set par   ""
   # H-bond parameters (Adjust this to your file location)
   set defhpar  "/projects/mdenergy/hbonds/par_hbond.inp"
   set hpar   ""
   set psf   ""
   set sfile ""
   set stype ""
   set cfile ""
   set ctype ""
   set ofile "/dev/tty"  
   set afile ""
   set veldcd ""
   set avg 0
   set avgmode ""
   set switch 10
   set cutoff 12
   set self  ""
   set beg   [molinfo top get frame]
   set end   [molinfo top get frame]
   set nsel 0
   set sel1 ""
   set sel2 ""
   set energy ""
   set visual 0
   set spawn "&"
   set pat   ""
   set top   ""
   set hpsf  ""

   # Get coordinate and structure files from VMD
   foreach i [join [molinfo top get filetype]] j [join [molinfo top get filename]] {
      if {$i=="psf" || $i=="parm7"} {
	 set sfile $j
	 set stype $i
      }
      if {$i=="pdb" || $i=="dcd"} {
	 set ctype $i
	 set cfile $j
      }
   }
   if {$stype=="parm7"} { set par "-amber $sfile" }
   if {$stype=="psf"}   { set psf "-psf $sfile"   }

   # Scan for single options
   set argnum 0
   set arglist $args
   set energylist {-all -bond -angl -dihe -impr -vdw -elec -nonb -conf -hbon -kin}
   foreach i $args {
      if {$i=="-self"}  then { 
	 set self "-self" 
	 set arglist [lreplace $arglist $argnum $argnum] 
	 continue
      }
      if {$i=="-visual"}  then { 
	 set visual 1 
	 set spawn ""
	 set arglist [lreplace $arglist $argnum $argnum] 
	 continue
      }
      if {[lsearch $energylist [string range $i 0 4]]>=0}  then { 
	 set energy $i 
	 puts $argnum
	 set arglist [lreplace $arglist $argnum $argnum] 
	 continue
      }
      if {$i=="-sel"}  then { 
	 set upper [expr $argnum+1]
	 set sel1 [lindex $arglist $upper]
	 set nsel 1
	 set next [lindex $arglist [expr $argnum+2]]
	 if {[string match "-*" $next]!=1 && [string length $next]>0} {
	    set upper [expr $argnum+2]
	    set sel2  [lindex $arglist $upper]
	    set nsel 2
	 }
	 set arglist [lreplace $arglist $argnum $upper]  
	 incr argnum [expr $argnum-$upper]
	 continue
      }
      incr argnum
   }

   if {![llength $energy]} {
      error "No energy type specified!\nUse one of \[$energylist\]"
   }

   set nonblist {-vdw -elec -nonb}
   if {$nsel==2 && [lsearch $nonblist $energy]<0} {
      error "Interaction energy can only be computed for -vdw, -elec or -nonb!"
   }

   # Scan for options with one argument
   set argnum 0
   set otherarglist {}
   foreach {i j} $arglist {
      if {$i=="-beg"}   then { set beg $j; continue }
      if {$i=="-end"}   then { set end $j; continue  }
      if {$i=="-par"}   then { 
	 foreach file $j {
	    append par " -par $file"
	 }
	 continue
      }
      if {$i=="-amber"} then { set par "-amber $j"; set stype="parm7"; continue  }
      if {$i=="-xplor"} then { set par "-xplor $j"; set stype="psf"; continue  }
      if {$i=="-hpar"}  then { set defhpar "$j"; continue  }
      if {$i=="-pat"}   then { set pat "$j"; continue  }
      if {$i=="-top"}   then { set top "$j"; continue  }
      if {$i=="-ofile"} then { set ofile $j; continue  }
      if {$i=="-afile"} then { set afile $j; continue  }
      if {$i=="-avg"}   then { set avg $j; continue  }
      if {$i=="-switch"} then { set switch $j; continue  }
      if {$i=="-cutoff"} then { set cutoff $j; continue  }
      if {$i=="-vel"}   then { set veldcd $j; continue  }
      if {$i=="-dcd"}   then { set cfile $j; set ctype dcd; continue  }
      if {$i=="-pdb"}   then { set cfile $j; set cfile pdb; continue  }
      if {$i=="-avgmode" && $j=="ramp"} then { set avgmode "-ramp"; continue  }
      if {$i=="-avgmode" && $j=="pad"}  then { set avgmode "-pad"; continue  }
      lappend otherarglist $i $j
   }

   
   if {$end=="last"} {set end [expr [molinfo top get numframes] -1]}

   if {![llength $par]} {
      if {[file exists $defpar]} {
	 puts "Using default parameter file (charmm stype):"
	 puts $defpar
	 set par "-par $defpar"
      } else {
	 puts $defpar
	 error "No parameter file given, default parameter file not found:"
      }
   } else {
#       set newpar {}
#       foreach file $par {
# 	 append newpar " -par $file"
#       }
#       set par $newpar
   }

   if {[string range $energy 0 4]=="-hbon"} {
      set hpar "-hpar $defhpar"
      set top  "-top $top"
      #set hpsf $psf
      #set psf "[regsub ".psf" $psf ""]+hbonds.psf"
   }

   if {[string range $energy 0 4]=="-kin"} {
      if {![llength $veldcd]} {
	 error "If you are using -kin, you must specify a velocity DCD file with -veldcd."
      } else {
	 set veldcd "-vel $veldcd"
      }
   }

   if {[llength $afile]} {
      set afile "-a $afile"
   }
   if {![llength $afile] && $visual} {
      set afile "-a energy_per_atom.dat"
   } 

   if {($stype!="psf" && $stype!="parm7")} {
      error "No structure file (psf/parm7) found!"
   }
   if {!($ctype=="pdb" || $ctype=="dcd")} { 
      error "No coordinate file (pdb/dcd) found!"
   }

   if {$nsel==0} {
      error "No selection specified!"
   }

   set s1 "MDENERGY_1.sel"
   write_sel $sel1 $s1

   if {$nsel==2} {
      if {$self=="-self"} {
	 error "Specifing -self with two selections makes no sense!"
      }
      if {$visual} {
	 error "Visuaization for interaction energy not (yet) available!"
      }
      set s2 "MDENERGY_2.sel"
      write_sel $sel2 $s2
      set selection "-sel $s1 -sel $s2"
      puts "\nComputing interaction energy between:"
      puts "[$sel1 text]"
      puts "and"
      puts "[$sel2 text]\n"
   } else {
      set selection "-sel $s1"
      puts "Computing energy for selection:"
      puts "[$sel1 text]\n"
   }

   # Build the option string
   set opt1 "$energy $selection -$ctype $cfile $psf $par -beg $beg -end $end "
   set opt2 "$self -avg $avg $avgmode -switch $switch -cutoff $cutoff "
   set opt3 "$veldcd $afile $hpar $otherarglist"
   set options [concat $opt1 $opt2 $opt3]

   if {[string range $energy 0 4]=="-hbon"} {
       #puts "Running:"
       #puts "$HBP_RUN $hpsf $hpar $top $pat"
       #eval exec $HBP_RUN $hpsf $hpar $top $pat
   }

   # Tell the user what's happening
   puts "Running:"
   puts "$MDE_RUN $options > $ofile 2> /dev/tty $spawn\n"
   
   # Run MDEnergy
   eval "exec $MDE_RUN $options > $ofile 2> /dev/tty $spawn"

   # Visualize energies in VMD
   if {$visual} {
      if {[string range $energy 0 4]=="-hbon"} {
	 puts "Running:"
	 puts "visual_hbonds hbfile \n"
	 visual_hbonds hbfile
      } else {
	 set atom_energy_file [regsub "^-a " $afile ""]
	 puts "Running:"
	 puts "visual_mdenergy $atom_energy_file \n"
	 viz_energy $atom_energy_file
      }
   }

   # Cleanup files
   # after idle {file delete MDENERGY_1.sel MDENERGY_2.sel}

   puts "(You can kill the process with 'enstop' or 'energy stop')"
}

proc enstop {} {
  global MDENERGY_PID
  set MDENERGY_PID [lindex [exec ps -ef | grep "mdenergy" | grep -v grep] 1]
  if {$MDENERGY_PID!=0} {
     exec kill -9 $MDENERGY_PID
     puts "Killed process $MDENERGY_PID"
     set MDENERGY_PID 0
  }
}

proc write_sel {sel file {molid top}} {
    set fid [open $file w]
    set seltext [$sel text]
    puts $fid "selectiontext $seltext"
    puts $fid [$sel list]
    flush $fid
    close $fid
}
 

# Determine type of machine, and the appropriate executable
proc get_machine_arch { } {
   set macharch [exec uname -s]
   return $macharch
}
