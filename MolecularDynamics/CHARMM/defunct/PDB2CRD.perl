#!/usr/bin/perl -w
# PERL script to add fixed atom flag to backbone atoms for
# NAMD run. Only "ATOM" records in input. CHC 1/21/05.
while (defined ($line = <>)) {
    chomp($line);
    if ( $line eq "END" ) {
        print $line;
       } else {
        my($junk1, $atomid, $junk2, $atomname, $restype, $residue, $junk3, $x, $y, $z) =
            unpack("A4 A7 A2 A4 A3 A6 A4 A8 A8 A8", $line);
#        $out_line = pack ("A5 A5 A1 A5 A4 A10 A10 A10", $atomid, $residue, " ", $restype,
#                        $atomname, $x, $y, $z);
        printf "%5d%5d%1s%-5s%-4s%10.5f%10.5f%10.5f\n", $atomid, $residue, " ", $restype,
              $atomname, $x, $y, $z;
        }
    }

