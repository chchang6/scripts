#!/bin/sh
rm ! namd2.*.pbs *.restart.* sideeq_out.vel
mkdir sideeq
mv sideeq* sideeq/.
cp sideeq/sideeq_out.coor ./alleq_in.coor
cp sideeq/sideeq_out.xsc ./alleq_in.xsc
sed -f ../temp.sed equilibrate_mobile.namd > temp
mv temp equilibrate_mobile.namd
sed -f ../temp.sed equilibrate_mobile.pbs > temp
mv temp equilibrate_mobile.pbs

