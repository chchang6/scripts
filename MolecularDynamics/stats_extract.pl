#!/usr/bin/perl
# PERL Script to rearrange columns in an input file.
while (<>) {
   chomp;
   @array = split /\s+/;
   if ($array[0] eq "ETITLE:") {
      printf "%4s%11s%14s%14s%12s%13s%13s\n", $array[1], $array[6], $array[7],
         $array[10], $array[11], $array[13], $array[14];
   } else {
      printf "%-6d%13.4f%13.4f%13.4f%13.4f%13.4f%13.4f\n", $array[1], $array[6], $array[7],
         $array[10], $array[11], $array[13], $array[14];
   }
}

