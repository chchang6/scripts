mol new 2Z5Rfull.pdb
set stuff [atomselect top all]
set chainstring 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
set topnum 1422
set numchains 24
for {set i 0} {$i < $numchains} {incr i} {
  set firstatom [expr $i * $topnum]
  set lastatom [expr $firstatom + $topnum - 1]
  set temp [atomselect top "index $firstatom to $lastatom"]
  $temp set chain [string index $chainstring [expr $i+1]]
  puts -nonewline "Done with chain "
  puts $chain
}
$stuff writepdb test.pdb
mol delete all