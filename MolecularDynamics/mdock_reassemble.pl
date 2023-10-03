#!/usr/bin/perl -w
# PERL script to reassemble a PDB file from the pre- and post-
# MULTIDOCK files. The post-MULTIDOCK file should have been cleaned
# up first so residue numbers do not have appended letters, and the
# N-terminal modifications of the chains are removed. Chains are assumed
# to be specified numerically, as required for MULTIDOCK to run.
# CHC 1/12/05.
#
print "The old input file should have the last TER record deleted prior to\n";
print "running this script; otherwise, delete the last output record.\n";
print "The MULTIDOCK output file should have been edited manually to\n";
print "remove letters from the residue numbers and to fix the N-terminal\n ";
print "modifications.\n";
# Assigning input and output files
$INFILE1 = $ARGV[1];
$INFILE2 = $ARGV[3];
$OUTFILE = $ARGV[5];
$atmidx = 1;
$flag = 0;
# Open input and output files
open INFILE1, "<$INFILE1" or die "Pre-multidocked file not found";
open INFILE2, "<$INFILE2" or die "Multidocked PDB file not found";
open OUTFILE, ">$OUTFILE" or die "Can not open output file--check directory
permissions or preexisting file with same name.";
while ( defined ( $input1 = <INFILE1> ) ) {
    chomp $input1;
    if ( $flag == 0 ) {
       chomp ( $input2 = <INFILE2> );
    }
    @fields1 = split /\s+/, $input1;
    @fields2 = split /\s+/, $input2;
    if ($fields1[0] eq 'TER') {
        chomp ( $input1 = <INFILE1> );
        @fields1 = split /\s+/, $input1;
    }
    if ($fields2[2] eq 'HN') {
        chomp ( $input2 = <INFILE2> );
        @fields2 = split /\s+/, $input2;
    }
# Test atom type and residue number between the two files. If they are
# equal, print out the record for the new file, which contains the same
# atom in either the same position, or an updated position.
# The flag is (re)set to 0 to ensure the next while loop cycle results in
# Reading new lines from both input files.
    if ( ($fields1[2] eq $fields2[2]) && ($fields1[5] == $fields2[5]) ) {
          printf OUTFILE "%-6s%5d%2s%-3s%1s%-4s%1d%4d%4s%8.3f%8.3f%8.3f\n",
               'ATOM', $atmidx, ' ', $fields2[2], ' ', $fields2[3], $fields2[4],
               $fields2[5], ' ', $fields2[6], $fields2[7], $fields2[8];
          $flag = 0;
          $atmidx++;
       }
# Now need to handle the case where the first conditional is true, but the
# second not true. This occurs when there is a switch to a new residue lacking
# in the new file but present in the old. The CA atom is not printed
# because the above outer loop is true, but the inner false, so nothing
# is printed, and the else clause below is not executed because the outer
# loop above is true. Print out old file line.
    elsif ( ($fields1[2] eq $fields2[2]) && ($fields1[5] != $fields2[5]) ) {
             printf OUTFILE "%-6s%5d%2s%-3s%1s%-4s%1d%4d%4s%8.3f%8.3f%8.3f\n",
                  'ATOM', $atmidx, ' ', $fields1[2], ' ', $fields1[3],
                  $fields1[4], $fields1[5], ' ', $fields1[6], $fields1[7],
                  $fields1[8];
             $flag = 0;
             $atmidx++;
          }
# If neither is the case, then the record from the old file must be for
# a residue that was not included in the simulation. If so, the old file
# record should be printed out, a new record read from the old file, and
# a new comparison made. The flag is set to 1 to allow reading from only
# the old file at the beginning of the while loop.
    else {
       printf OUTFILE "%-6s%5d%2s%-3s%1s%-4s%1d%4d%4s%8.3f%8.3f%8.3f\n",
            'ATOM', $atmidx, ' ', $fields1[2], ' ', $fields1[3], $fields1[4],
            $fields1[5], ' ', $fields1[6], $fields1[7], $fields1[8];
       $flag = 1;
       $atmidx++;
       }
}
close INFILE1;
close INFILE2;
close OUTFILE;
print "Don't forget to add fix replace any residue coordinates that were ";
print "active in the MULTIDOCK run that you want fixed with the old file ";
print "coordinates.\n";
