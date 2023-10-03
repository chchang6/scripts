PROGRAM PNLMO_PARSER
! Fortran program to read in (P)NLMO data from an NBO 5.0 "AO(P)NLMO" job
! and create file of this data in a format suitable for direct pasting
! into a Gaussian 2003 formatted checkpoint file. Assumes number of
! (P)NLMOs equals the number of AOs, which should be true unless NBO
! eliminates some due to linear dependency. CHC  07/15/05.
!
IMPLICIT NONE
REAL, ALLOCATABLE, DIMENSION (:,:) :: array
INTEGER :: ierror, iostat, i, j, num, number_of_full_blocks
INTEGER :: number_of_leftover_orbitals
CHARACTER(len=50) :: input, output
! Get total number of orbitals
WRITE (*,*) "Enter the number of (P)NLMOs in the input file:"
READ (*,*), num
! Calculate the dimensions of the file, assuming standard NBO 5.0g output
! format, 7 (P)NLMOs per line. Allocate array
number_of_full_blocks = num / 7
number_of_leftover_orbitals = MOD(num,7)
ALLOCATE (array(1:num, 1:num), STAT=iostat)
! Get input and output file names from user
WRITE (*,*) "Enter name of input file:"
READ (*,*) input
WRITE (*,*) "Enter name of output file:"
READ (*,*) output
! Open file for input
OPEN (UNIT=5, FILE=input, STATUS='OLD', ACTION='READ', IOSTAT=ierror)
! Read in first header line, which I like to leave in for verification
! purposes, should read " PNBOs in the AO basis:"
READ (5,*)
! Loops to read in the input data into matrix "array"
DO i = 1, number_of_full_blocks, 1
   READ (5,*)
   READ (5,*)
   READ (5,*)
   DO j = 1, num, 1
      READ (5,100) array(j,((i-1)*7+1)), array(j,((i-1)*7+2)), &
array(j,((i-1)*7+3)), array(j,((i-1)*7+4)), array(j,((i-1)*7+5)), &
array(j,((i-1)*7+6)), array(j,((i-1)*7+7))
100   FORMAT (16X,7F9.4)
   END DO
END DO
! Loops to read in remaining input data
IF (number_of_leftover_orbitals /= 0) THEN
   READ (5,*)
   READ (5,*)
   READ (5,*)
   DO j = 1, num, 1
      DO i = 7*number_of_full_blocks+1, 7*number_of_full_blocks+   &
   number_of_leftover_orbitals, 1
   IF (number_of_leftover_orbitals == 1) THEN
      READ (5,'(16X,F9.4)') array(j,i)
   ELSE IF (number_of_leftover_orbitals == 2) THEN
      READ (5,'(16X,2F9.4)') array(j,i)
   ELSE IF (number_of_leftover_orbitals == 3) THEN
      READ (5,'(16X,3F9.4)') array(j,i)
   ELSE IF (number_of_leftover_orbitals == 4) THEN
      READ (5,'(16X,4F9.4)') array(j,i)
   ELSE IF (number_of_leftover_orbitals == 5) THEN
      READ (5,'(16X,5F9.4)') array(j,i)
   ELSE IF (number_of_leftover_orbitals == 6) THEN
      READ (5,'(16X,6F9.4)') array(j,i)
   ELSE
      READ (5,'(16X,7F9.4)') array(j,i)
   END IF
   END DO
END DO
END IF
! Close input file
CLOSE (UNIT=5)
! Open file for output
OPEN (UNIT=6, FILE=output, STATUS='NEW', ACTION='WRITE', IOSTAT=ierror)
! Dump data in "array" in Gaussian fchk format
WRITE (6,'(5E16.8)') ( (array (j,i), j = 1, num), i = 1, num )
CLOSE (UNIT=6)
DEALLOCATE (array, STAT=iostat)
END PROGRAM PNLMO_PARSER
