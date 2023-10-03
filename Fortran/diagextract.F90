PROGRAM diagextract
! Program to extract the diagonal elements of the second derivative matrix
! output in PES.out using Gaussian 2003 IOp 7/32=3. Gaussian ouput
! is the lower diagonal matrix.
IMPLICIT NONE
REAL, ALLOCATABLE, DIMENSION(:,:) :: forceconstants
REAL :: junk
INTEGER :: i, j, ierror, status, user
WRITE (*,*) 'How many force constants to extract from file ForceMatrix (0 to quit)?'
READ (*,*) user
IF (user == 0) STOP 'Terminated by user input'
ALLOCATE (forceconstants(user,user), STAT=status)
OPEN (UNIT=10, FILE='ForceMatrix', STATUS='OLD', ACTION='READ', IOSTAT=ierror)
READ (10,*)
READ (10,100) ((forceconstants(i,j), j=1, i), i = 1, user)
100   FORMAT (5F20.12)
CLOSE (UNIT=10)
OPEN (UNIT=11, FILE='ForceConstants', STATUS='NEW', ACTION='WRITE', IOSTAT=ierror)
WRITE (11,110) (i, forceconstants(i,i), i=1,user)
110 FORMAT ('Internal coordinate ',I4, ' force constant(amu): ', F20.12)
CLOSE (UNIT=11)
DEALLOCATE (forceconstants, STAT=status)
END PROGRAM diagextract
