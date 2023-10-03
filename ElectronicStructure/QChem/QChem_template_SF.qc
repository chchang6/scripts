$comment
  Squared gradient minimization with fragment guess for delta-SCF
  antiferromagnetic 4-spin  dimer, sulfurs opposing
  meta-GGA SCAN/def2-TZVPP
$end
 
$molecule
0 1
--
0 3
--
0 -3
$end

$rem
   method scan
   unrestricted true
   basis def2-TZVPP
   scf_guess fragmo
   fragmo_guess_mode 0
   scf_print 1
   scf_print_frgm true
   scf_algorithm sgm_ls
   delta_gradient_scale 100
   mem_total 50000
   mem_static 400
   max_scf_cycles 500
$end

$rem_frgm
   scf_algorithm diis
$end

@@@

$comment
  Ferromagnetic 4-spin  dimer, sulfurs opposing
  meta-GGA SCAN/def2-TZVPP
$end
 
$molecule
0 5
--
0 3
--
0 3
$end

$rem
   jobtype sp
   method scan
   unrestricted true
   basis def2-TZVPP
   scf_guess fragmo
   scf_print 1
   mem_total 50000
   mem_static 400
$end

