# Small adaptation of script supplied to VMD mailing list by
# Eduard Schreiner, subject "Re: dihedral angles, Tue Dec 06 2005.
animate read dcd 0-1.0ns.dcd waitfor all top
mol addfile nowaterions.psf
animate goto start
#animate delete beg 0 end 0 0
#animate goto start

set fp [open "HYDD_Fe1S1Fe2S2.txt" w]
set ts 0
# Here place the molecule and atom indices you want
# (check the manual for 'label add' command)
label add Dihedrals 0/8938 0/8942 0/8939 0/8943
foreach dihed [label graph Dihedrals 0] {
    incr ts
    puts $fp [format "%12.5f %12.5f" $ts $dihed]
}
close $fp
unset fp
unset dihed 
