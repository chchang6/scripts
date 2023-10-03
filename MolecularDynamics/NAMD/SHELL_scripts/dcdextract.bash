#!/bin/bash
infile=dyn_2.2ns_out.dcd
outfile=quasi_20001-22000.dcd
for ((i=0; i < 10; i += 1))
do
   /copt/namd2/2.6b1/bin/catdcd -o temp_$i.dcd -otype dcd -i indexfile -first $[$i*200+1] -last $[($i+1)*200] -dcd $infile
done
#
for ((i=0; i < 9; i += 1))
do
   /copt/namd2/2.6b1/bin/catdcd -o new.dcd -otype dcd temp_$i.dcd temp_$[$i+1].dcd
   mv new.dcd temp_$[$i+1].dcd
   rm temp_$i.dcd
done

mv temp_9.dcd $outfile
