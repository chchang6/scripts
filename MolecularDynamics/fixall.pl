#!/usr/bin/perl -w
# PERL script to add fixed atom flag to backbone atoms for
# NAMD run. Only "ATOM" records in input. CHC 1/21/05.
while (defined ($line = <>)) {
    chomp($line);
    if ( $line eq "END" ) {
        print $line;
       } else {
        my($atomid, $restype, $residue, $beta, $mol) = unpack("A17 A4 A41 A4 A10",
           $line);
        $out_line = pack ("A17 A4 A41 A4 A10", $atomid, $restype, $residue,
                        "1.00", $mol);
        print "$out_line\n";
        }
    }
