#!/usr/bin/perl
# PERL script to go through inidividual extracted sections of PSF file
# (bond, angle, dihedral, improper) and change atom numbers. Useful
# to convert NAMD patch order to canonical for CHARMM analysis.
# CHC 08/01/05
while (<>) {
   chomp;
   @line = split /\s+/, $_;
   printf "%5d", $line[1]-1;
}
printf "\n", " ";
