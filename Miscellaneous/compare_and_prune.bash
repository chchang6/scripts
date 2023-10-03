#!/bin/bash
# Script to compare versions of scripts between 2 locations, and get rid of
#   duplicates in location2.

location1=/path/to/location/1
location2=/path/to/location/2

for i in `ls $location1`
do
   if [ -f $location1/$i ]
   then
      if [ ! -f $location2/$i ]
      then
         continue
      fi
      if diff -q $location1/$i $location2/$i
      then
         echo "No difference between $location1/$i and $location2/$i"
         rm -f $location2/$i
      else
         echo "$location1/$i"
         ls -l $location1/$i
         echo "$location2/$i"
         ls -l $location2/$i
         diff $location1/$i $location2/$i
      fi
   fi
done

for i in `ls $location2`
do
   if [ -f $location2/$i -a ! -f $location1/$i ]
   then
      echo "Found $location2/$i not in " `dirname $location1/$i`
   fi
done

