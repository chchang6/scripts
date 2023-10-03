#!/bin/bash
egrep -m 1 '^ETITLE' sideeq.log > ./stats.txt
egrep '^ENERGY' sideeq.log >> ./stats.txt
