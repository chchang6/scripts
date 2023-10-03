#!/usr/bin/perl
# PERL script to go through inidividual extracted sections of PSF file
# (bond, angle, dihedral, improper) and change atom numbers. Useful
# to convert NAMD patch order to canonical for CHARMM analysis.
# CHC 08/01/05
@header=split /\n+/, $_;
$numthings = $header[1];
$type = $header[3];
$leastatom =
$greatestatom =
while (<>) {
   chomp;
   if ($type eq "bonds") {
   @line = split /\s+/, $_;
   $index = 1
   foreach $line (@line) {
      if ($line == 5503) {
         $line = 5510;
      } elsif ($line == 5504) {
         $line = 5507;
      } elsif ($line == 5505) {
         $line = 5503;
      } elsif ($line == 5506) {
         $line = 5504;
      } elsif ($line == 5507) {
         $line = 5505;
      } elsif ($line == 5508) {
         $line = 5506;
      } elsif ($line == 5509) {
         $line = 5508;
      } elsif ($line == 5510) {
         $line = 5509;
      }
   }
#   printf "%8d%8d%8d%8d%8d%8d%8d%8d\n", $line[1], $line[2], $line[3], $line[4],
#         $line[5], $line[6], $line[7], $line[8]; # bonds, dihedrals, impropers
#}
   printf "%8d%8d%8d%8d%8d%8d%8d%8d%8d\n", $line[1], $line[2], $line[3], $line[4],
         $line[5], $line[6], $line[7], $line[8], $line[9]; # angles
}
