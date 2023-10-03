#!/usr/bin/perl -w
# PERL script to swap columns in a tab-delimited file,
# such as typically producible by Microsoft Escel.
# CHC 1/6/05.
$i = 0;
while (<>) {
   $i=$i+1;
   @array = split /\s+/, $_;
   if ($i%10 != 0) {
      printf "%5i", $array[1]-1;
   } else {
      printf "%5i\n", $array[1]-1;
   }
}
print "\n";
