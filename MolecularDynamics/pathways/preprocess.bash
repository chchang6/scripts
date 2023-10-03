#!/bin/bash
# Script to preprocess MPI Pathways output file. Should be first thing run. CHC 03/18/09
LOGFILE=log002
OUTFILE=pre_002.log
# Find lines starting with "Pathway" or accidentally split lines from MPI output
grep '^[P0-9]' $LOGFILE | \
# Remove frame data with no pathways found
sed '/is: $/d' | \
# Remove spurious MPI output, which seems to be limited to "Sent rank" messages
sed 's/Sent.*$//' | \
# Now replace new lines with exclamation points.
tr '\012' '!' | \
# Join the lines that MPI accidentally split...
sed 's/\([0-9]\)!\([0-9]\)/\1\2/g' | \
# ... and change exclamations back to newlines.
tr '!' '\012' > $OUTFILE
