#!/bin/ksh
timeold="2.2ns"
timenew="2.4ns"
if [[ -z `diff dyn_${timeold}_out.coor dyn_${timeold}_out.restart.coor` ]] &&
   [[ -a dyn_${timeold}_out.coor ]]; then
   rm *.restart.* dyn_${timeold}_in.* dyn_${timeold}_out.xst
   rm stats.txt namd2.* nodelist dyn_${timeold}.log.gz
   for x in coor vel xsc
   do
      mv dyn_${timeold}_out.$x dyn_${timenew}_in.$x
   done
   else print 'There is a difference between the output and restart coordinates!'
fi
