#!/usr/bin/perl -w
# PERL script to calculate means and standard deviations
# of GBMV energy arrays. Assume CHARMM output file from
# GBMV run named "GBMVdyn.out".
# See notebook112806-120206.doc for regex and rewrite
# using PERL regular expressions. CHC 12/1/06.
BEGIN { push(@INC, "/uhome/cchang/PERL_modules") }
use Math::NumberCruncher;
open TOTAL, "<GBMVdyn.out"
  or die "No such file fullenergies.";
while (<TOTAL>) {
   chomp;
   if (/^ENER>/) {
      @temp = split /\s+/, $_;
      push(@total, $temp[2]);
   } elsif (/^ENER PBEQ>/) {
      @temp = split /\s+/, $_;
      push(@gb, $temp[4]);
   }
}
close TOTAL;
$numelements = @total;
@internal = 1..$numelements;
for ($i = 0; $i < $numelements; $i++) {
   $internal[$i] = $total[$i] - $gb[$i];
}
$av_total = Math::NumberCruncher::Mean(\@total);
$av_GB = Math::NumberCruncher::Mean(\@gb);
$av_internal = Math::NumberCruncher::Mean(\@internal);
$std_total = Math::NumberCruncher::StandardDeviation(\@total);
$std_GB = Math::NumberCruncher::StandardDeviation(\@gb);
$std_internal = Math::NumberCruncher::StandardDeviation(\@internal);
print "Average total energy over trajectory = ",$av_total," kcal/mol.\n";
print "Standard deviation for total energy = +/-",$std_total," kcal/mol.\n";
print "Average GB solvation energy over trajectory = ",$av_GB," kcal/mol.\n";
print "Standard deviation for GB solvation energy = +/-",$std_GB," kcal/mol.\n";
print "Average internal energy over trajectory = ",$av_internal," kcal/mol.\n";
print "Standard deviation for internal energy = +/-",$std_internal," kcal/mol.\n";
