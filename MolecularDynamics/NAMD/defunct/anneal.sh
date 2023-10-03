#!/bin/sh
rm ! namd2.*.pbs *.restart.*
mkdir anneal
mv anneal_[io]*.* anneal/.
mv simanneal.* anneal/.
chmod 444 anneal/*
