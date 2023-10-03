#!/usr/bin/perl
# PERL script to parse the dihedral angle section of a NAMD PSF
# file to one-index-per-line format, for input into get_dihe_energies.vmd.
# CHC 12/07.
while (<>) {
   chomp;
   @line = split /\s+/, $_;
   for ($i = 1; $i <=8; $i++) {
      print "$line[$i]\n";
   }
}
