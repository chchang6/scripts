#!/usr/bin/perl -w
# PERL script to renumber PDB file to make consecutive
# atom and residue numbers. File must be only ATOM records,
# contain no alternate locations, and comprise only one
# chain--no chain identifier can be present, as this will
# mess up the parsing of the fields. CHC 1/6/05.
$atmidx = 0;
$residx = 1;
$linidx = 1;
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
         if ($restest ne $resref) {
             $residx++;
             $resref = $fields[4];
             }
# Print statements
         if (length $fields[2] == 4) {
            printf "%-4s%7d%1s%4s%4s%6d%12.3f%8.3f%8.3f%6.2f%6.2f\n",
            'ATOM', $atmidx, ' ', $fields[2], $fields[3], $residx,
            $fields[5], $fields[6], $fields[7], $fields[8], $fields[9];
            } else {
            printf "%-4s%7d%2s%-3s%4s%6d%12.3f%8.3f%8.3f%6.2f%6.2f\n",
            'ATOM', $atmidx, ' ', $fields[2], $fields[3], $residx,
            $fields[5], $fields[6], $fields[7], $fields[8], $fields[9];
            }
         $linidx++;
       }
}
