#!/bin/bash

for i in `ipcs -s | grep $USER | cut -f2 -d" "`
do
   ipcrm -s $i
done
for i in `ipcs -m | grep $USER | cut -f2 -d" "`
do
   ipcrm -m $i
done

