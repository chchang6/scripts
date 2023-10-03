#!/usr/bin/perl
# PERL script to analyze the output from "get_dihe_energies.vmd".
# CHC 12/13/07.
{
 open FILE, $ARGV[0];
   @stuff = <FILE>;
 close FILE;
 while(@stuff) {
 $data = pop(@stuff);
 $junk = pop(@stuff);
 $indices = pop(@stuff);
 @dihedrals = split /\s+/, $data;
 chomp($indices);
 $hash{$indices} = $dihedrals[2];
 }
 sub numeric_sort { $hash{$b} <=> $hash{$a} }
 foreach $key (sort numeric_sort (keys(%hash))) {
  print $key, ",  Dihedral energy: ", $hash{$key}, "\n"
 }
}
