#!/bin/sh
rm ! namd2.*.pbs *.restart.*
mkdir alleq
mv alleq* alleq/.
cp alleq/alleq_out.vel ./anneal_in.vel
cp alleq/alleq_out.coor ./anneal_in.coor
cp alleq/alleq_out.xsc ./anneal_in.xsc
cp ../simanneal.* .

