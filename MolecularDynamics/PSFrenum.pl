#!/usr/bin/perl
# PERL script to go through inidividual extracted sections of PSF file
# (bond, angle, dihedral, improper) and change atom numbers. Useful
# to convert NAMD patch order to canonical for CHARMM analysis.
# CHC 08/01/05
while (<>) {
   chomp;
   @line = split /\s+/, $_;
   foreach $line (@line) {
      if ($line == 7944) {
         $line = 7941;
      } elsif ($line == 7945) {
         $line = 7942;
      } elsif ($line == 7946) {
         $line = 7943;
      } elsif ($line == 7947) {
         $line = 7944;
      } elsif ($line == 7948) {
         $line = 7945;
      } elsif ($line == 7949) {
         $line = 7946;
      } elsif ($line == 7950) {
         $line = 7947;
      } elsif ($line == 7951) {
         $line = 7948;
      } elsif ($line == 7952) {
         $line = 7949;
      } elsif ($line == 7953) {
         $line = 7950;
      } elsif ($line == 7954) {
         $line = 7951;
      } elsif ($line == 7955) {
         $line = 7952;
      } elsif ($line == 7956) {
         $line = 7953;
      } elsif ($line == 7957) {
         $line = 7954;
      } elsif ($line == 7958) {
         $line = 7955;
      } elsif ($line == 7959) {
         $line = 7956;
      } elsif ($line == 7960) {
         $line = 7957;
      } elsif ($line == 7961) {
         $line = 7958;
      } elsif ($line == 7962) {
         $line = 7959;
      } elsif ($line == 7941) {
         $line = 7960;
      } elsif ($line == 7942) {
         $line = 7961;
      } elsif ($line == 7943) {
         $line = 7962;
      }
   }
#   printf "%8d%8d%8d%8d%8d%8d%8d%8d\n", $line[1], $line[2], $line[3], $line[4],
#         $line[5], $line[6], $line[7], $line[8]; # bonds, dihedrals, impropers
#}
   printf "%8d%8d%8d%8d%8d%8d%8d%8d%8d\n", $line[1], $line[2], $line[3], $line[4],
         $line[5], $line[6], $line[7], $line[8], $line[9]; # angles
}
