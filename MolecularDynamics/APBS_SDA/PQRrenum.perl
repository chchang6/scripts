#!/usr/bin/perl -w
# PERL script to renumber PQR file to make consecutive
# atom and residue numbers. File must be only ATOM records,
# contain no alternate locations, and comprise only one
# chain--no chain identifier can be present, as this will
# mess up the parsing of the fields. CHC 9/09/05.
$atmidx = 0;
$residx = 1;
$linidx = 1;
$sumcharge = 0;
while (<>) {
    chomp;
    @fields=split /\s+/, $_;
    if ($fields[0] eq "END") {
         print "$fields[0]\n";
       } elsif ($fields[0] eq 'ATOM') {
         if ($linidx == 1) {
            $resref = $fields[4];
            }
         $atmidx++;
         $restest = $fields[4];
         if ($restest != $resref) {
             $residx++;
             $resref = $fields[4];
             }
# Assign cluster charges and vdW parameters
         if ($fields[3] eq "HC1") {
            if ($fields[2] eq "FE1") {
               $fields[8] = -0.22; $fields[9] = 2.5;
            } elsif ($fields[2] eq "FE2") {
               $fields[8] = 0.1; $fields[9] = 2.5;
            } elsif ($fields[2] eq "S1" || $fields[2] eq "S2") {
               $fields[8] = -0.29; $fields[9] = 1.975;
            } elsif ($fields[2] eq "O3" || $fields[2] eq "O5" || $fields[2] eq "O7") {
               $fields[8] = -0.47; $fields[9] = 1.7;
            } elsif ($fields[2] eq "N4" || $fields[2] eq "N6") {
               $fields[8] = -0.51; $fields[9] = 1.85;
            } elsif ($fields[2] eq "C3" || $fields[2] eq "C5" || $fields[2] eq "C7") {
               $fields[8] = 0.5; $fields[9] = 1.8;
            } elsif ($fields[2] eq "C4" || $fields[2] eq "C6") {
               $fields[8] = -0.1; $fields[9] = 1.8;
            } elsif ($fields[2] eq "N1") {
               $fields[8] = -0.67; $fields[9] = 1.85;
            } elsif ($fields[2] eq "HN") {
               $fields[8] = 0.38; $fields[9] = 0.2245;
            } elsif ($fields[2] =~ /CB[13]/) {
               $fields[8] = -0.12; $fields[9] = 2.175;
            } else {
               $fields[8] = 0.09; $fields[9] = 1.32;
            }
         }
         if ($fields[3] eq "FS4") {
            if ($fields[2] =~ /FE[1-4]/) {
               $fields[8] = 0.64; $fields[9] = 2.5;
            } else {
               $fields[8] = -0.6; $fields[9] = 1.975;
            }
         }
         if ($fields[3] eq "FS2") {
            if ($fields[2] =~ /FE[12]/) {
               $fields[8] = 0.64; $fields[9] = 2.5;
            } else {
               $fields[8] = -0.56; $fields[9] = 1.975;
            }
         }
         if ($fields[3] eq "TIP3") {
            if ($fields[2] =~ /OH2/) {
               $fields[8] = -0.834; $fields[9] = 1.7682;
            } else {
               $fields[8] = 0.417; $fields[9] = 0.2245;
            }
         }
# Change cysteine patch charges
         if ($fields[3] eq "CYS") {
            if ($fields[4] == 69 || $fields[4] == 74 || $fields[4] == 77
                || $fields[4] == 107 || $fields[4] == 111 || $fields[4] == 166
                || $fields[4] == 366 || $fields[4] == 370) {
                if ($fields[2] eq "CB") {$fields[8] = -0.14;}
                if ($fields[2] eq "SG") {$fields[8] = -0.58;}
            }
         }
         $sumcharge = $sumcharge + $fields[8];
# Print statements
         if (length $fields[2] == 4) {
            printf "%-4s%7d%1s%4s%4s%6d%12.3f%8.3f%8.3f%8.4f%7.4f\n",
            'ATOM', $atmidx, ' ', $fields[2], $fields[3], $residx,
            $fields[5], $fields[6], $fields[7], $fields[8], $fields[9];
            } else {
            printf "%-4s%7d%2s%-3s%4s%6d%12.3f%8.3f%8.3f%8.4f%7.4f\n",
            'ATOM', $atmidx, ' ', $fields[2], $fields[3], $residx,
            $fields[5], $fields[6], $fields[7], $fields[8], $fields[9];
            }
         $linidx++;
       }
}
print "Sum of charges = $sumcharge";
