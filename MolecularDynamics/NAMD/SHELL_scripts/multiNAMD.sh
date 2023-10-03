#!/bin/sh
# Script to modify NAMD configuration file input filename according
# to filenames given by loop variable values and run NAMD. CHC 10/26/05
for (( x=-5; x <= 5; x += 1))
do
   for (( y=-5; y<=5; y += 1))
   do
      for (( z=-5; z<=5; z += 1))
      do
         sed -e "s/\(set inputname   \).*/\1 .\/${x}_${y}_${z}.pdb/" ./minimize.namd > ./temp
         mv ./temp ./minimize.namd
         echo "${x}_${y}_${z}.pdb" >> screen.log
         namd2 minimize.namd >> screen.log
         rm ./${x}_${y}_${z}.pdb
      done
      unset z
   done
   unset y
done
unset x
