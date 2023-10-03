#!/usr/bin/perl -w
# PERL script to add fixed atom flag to backbone atoms for
# NAMD run. Only "ATOM" records in input. CHC 1/21/05.
while (defined ($line = <>)) {
    chomp($line);
    my($atomid, $atomtype, $residue, $beta, $mol) = unpack("A12 A4 A46 A4 A10",
       $line);
    if (($atomtype eq ' N') || ($atomtype eq ' CA') || ($atomtype eq ' C')
        || ($atomtype eq ' O')) {
        $out_line = pack ("A12 A4 A46 A4 A10", $atomid, $atomtype, $residue,
                    "1.00", $mol);
         } else {
        $out_line = pack ("A12 A4 A46 A4 A10", $atomid, $atomtype, $residue,
                    "0.00", $mol);
         }
     print "$out_line\n";
     }
