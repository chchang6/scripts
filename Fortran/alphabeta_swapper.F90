PROGRAM alphabeta_swapper
! Program reads in alpha and beta MOs from parser output files into
! two arrays, allows swaps between arrays according to user input,
! then writes out new MO files for incorporation into a formatted checkpoint
! file. CHC 7/22/05
IMPLICIT NONE
REAL, ALLOCATABLE, DIMENSION (:,:) :: alpha_old, beta_old, alpha_new, beta_new
INTEGER :: ierror, iostat, i, j, num, alpha=1, beta
CHARACTER(len=20) :: inputa, inputb, test
! Get total number of orbitals
WRITE (*,*) "Enter the number of (P)NXOs in the alpha and beta input files:"
READ (*,*), num
ALLOCATE (alpha_old(1:num, 1:num), STAT=iostat)
ALLOCATE (beta_old(1:num, 1:num), STAT=iostat)
! Get input and output file names from user
WRITE (*,*) "Enter name of alpha input file:"
READ (*,*) inputa
WRITE (*,*) "Enter name of beta input file:"
READ (*,*) inputb
WRITE (*,*) "Output files will be named out_alpha and out_beta--OK to proceed(y/n)?"
READ (*,*) test
IF (test /= 'y') STOP

! Open files for input and read in data. Each MO is a column.
OPEN (UNIT=10, FILE=inputa, STATUS='OLD', ACTION='READ', IOSTAT=ierror)
READ (10,'5E16.8') alpha_old
CLOSE (UNIT=10)
OPEN (UNIT=11, FILE=inputb, STATUS='OLD', ACTION='READ', IOSTAT=ierror)
READ (11,'5E16.8') beta_old
CLOSE (UNIT=11)

! Fill new arrays with old orbitals
ALLOCATE (alpha_new(1:num, 1:num), STAT=iostat)
ALLOCATE (beta_new(1:num, 1:num), STAT=iostat)
alpha_new = alpha_old
beta_new = beta_old

! Take user input to swap orbitals
DO
   WRITE (*,*) "Enter alpha orbital to swap--if finished, enter 0:"
   READ (*,*) alpha
   IF (alpha == 0) EXIT
   WRITE (*,*) "Enter beta orbital to swap:"
   READ (*,*) beta
   DO i = 1, num
      alpha_new(i,alpha) = beta_old(i,beta)
      beta_new(i,beta) = alpha_old(i,alpha)
   END DO
   alpha_old = alpha_new
   beta_old = beta_new
END DO

! Write out swapped orbitals to files
OPEN (UNIT=10, FILE='out_alpha', STATUS='NEW', ACTION='WRITE', IOSTAT=ierror)
WRITE (10,'5E16.8') alpha_old
CLOSE (UNIT=10)
OPEN (UNIT=11, FILE='out_beta', STATUS='NEW', ACTION='WRITE', IOSTAT=ierror)
WRITE (11,'5E16.8') beta_new
CLOSE (UNIT=11)
DEALLOCATE (alpha_old, STAT=iostat)
DEALLOCATE (beta_old, STAT=iostat)
DEALLOCATE (alpha_new, STAT=iostat)
DEALLOCATE (beta_new, STAT=iostat)
END PROGRAM
