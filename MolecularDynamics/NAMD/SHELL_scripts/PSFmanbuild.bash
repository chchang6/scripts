#!/bin/bash
# Script to build the bonding section of a PSf file from renumbered
# sections made by PSFrenum.perl. Assumes section filenames in the
# cat statements, only numbers. See PSFrenum.perl for more details.
# The resultant "new.psf" will be tailed onto the atom section of
# the input PSf file (which has been manually renumbered).
filename="Hydferr42HSD.psf" # Change for particular case.

# Put bonds header into new file, followed by renumbered section and newline.
egrep 'bonds' $filename >> new.psf
cat newbonds >> new.psf
echo '' >> new.psf
# Put angles header into new file, followed by renumbered section and newline.
egrep 'angle' $filename >> new.psf
cat newangls >> new.psf
echo '' >> new.psf
# Put dihedrals header into new file, followed by renumbered section and newline.
egrep 'dihedrals' $filename >> new.psf
cat newdihes >> new.psf
echo '' >> new.psf
# Put impropers header into new file, followed by renumbered section and newline.
egrep 'impropers' $filename >> new.psf
cat newimprs >> new.psf
echo '' >> new.psf
# Add tail of H-bond donors, acceptors, and nonbonds. Assumes no useful
# information in these sections a la NAMD output. If PSF built by CHARMM,
# this part of script will not work (sections won't be renumbered).
sed -n '/donor/,$p' $filename >> new.psf
