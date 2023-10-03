
proc gettimestep {} {
  global inputname
  global runtype

  if {"$runtype" == "first"} {return 0} 

  set file [open "$inputname.xsc" "r"]

  set line [gets $file]
  set line [gets $file]
  set line [gets $file]
  close $file

  scan $line "%d" timestep
  return $timestep
}


#adjust number so that is it is a multiple of factor
proc makemultiple {factor number} {
  return [expr ($number/$factor+1)*$factor]
}

