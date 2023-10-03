#!/bin/csh

# Written in 1999 by Jim Phillips, Theoretical Biophysics Group,
# Beckman Institute, University of Illinois at Urbana-Champaign.

if ( $#argv < 1 ) then
  echo "Usage: $0 [zero] [diff] [<yfield> [<yfield> ...] [vs <xfield>]] <file>"
  exit -1
endif

set titles = `awk '/^ETITLE:/ { print; exit }' $argv[$#argv]`
echo $titles

if ( $#argv < 2 ) then
  echo "Usage: $0 [zero] [diff] [<yfield> [<yfield> ...] [vs <xfield>]] <file>"
  exit -1
endif

if ( $1 == zero ) then
  set zero = 1
  shift argv
else
  set zero = 0
endif

if ( $1 == diff ) then
  set zero = 1
  set diff = 1
  shift argv
else
  set diff = 0
endif

set ytargets =
while ( $#argv > 1 && $1 != vs )
  @ pos = 1
  foreach t ( $titles )
    if ( $t == $1 ) set ytargets = ( $ytargets $pos )
    @ pos++
  end
  shift argv
end

if ( $#ytargets == 0 ) exit -1

set xtarget = 2
if ( $1 == vs ) then
  shift argv
  @ pos = 1
  foreach t ( $titles )
    if ( $t == $1 ) set xtarget = $pos
    @ pos++
  end
  shift argv
endif

set file = $argv[1]

set ytitle =
foreach y ( $ytargets )
  set ytitle = ( $ytitle $titles[$y] )
end
set xtitle = $titles[$xtarget]

#echo Plotting $ytitle vs $xtitle
echo Calculating average of $ytitle

set title = $file

set open = '{'
set close = '}'
set dollar = '$'

if ( $zero ) then
  set subtitle = "change from initial value"
  set prog = "NR == 1 $open"
  foreach y ( $ytargets )
    set prog = "$prog z$y = $dollar$y;"
  end
  set prog = "$prog $close"
  set prog = "$prog $open print $dollar$xtarget"
  foreach y ( $ytargets )
    set prog = "$prog, $dollar$y - z$y"
  end
  set prog = "$prog $close"
  if ( $diff ) then
    set subtitle = "running backward difference"
    set prog = "$prog $open"
    foreach y ( $ytargets )
      set prog = "$prog z$y = $dollar$y;"
    end
    set prog = "$prog $close"
  endif
else
  set subtitle = ""
  set prog = "$open print $dollar$xtarget"
  foreach y ( $ytargets )
    set prog = "$prog, $dollar$y"
  end
  set prog = "$prog $close"
endif


set quote = '"'
set p_title = "TITLE $quote$title$quote"
set p_subtitle = "SUBTITLE $quote$subtitle$quote"
set p_xaxis = "XAXIS LABEL $quote$xtitle$quote"

set tmpfile = /tmp/namdplot.$USER.$$.tmp

set l_cmd = ( 0 0 0 0 0 0 0 0 0 0 )
@ pos = 1
foreach t ( $ytitle )
  @ i = $pos - 1
  set l_cmd[$pos] = "S$i LEGEND $quote$t$quote"
  @ pos++
end

while ( $pos <= 10 )
  set l_cmd[$pos] = "S$i LEGEND $quote$t$quote"
  @ pos++
end

grep '^ENERGY:' $argv | grep -v '[a-z]' | awk "$prog" > $tmpfile



set ys=`echo $ytitle | awk '{print NF}'`

echo $xtitle $ytitle >! data.dat
cat $tmpfile >> data.dat

