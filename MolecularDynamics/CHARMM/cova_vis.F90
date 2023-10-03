PROGRAM COVA_SORT
! Fortran program to create an atom-indexed list of covariance values
! to sort. Necessary input is (1) an ordered list of atom indices used
! to create the matrix, and the matrix file "covar.matrix". User is 
! prompted for the filename of the index list and output filename.
! Output is an ASCII file in the form of (atom1, atom2, covariance).
! CHC 050206
!
IMPLICIT NONE
INTEGER, ALLOCATABLE, DIMENSION (:) :: atomnumbers
REAL, ALLOCATABLE, DIMENSION (:,:) :: covar
REAL :: lowbin, highbin
INTEGER :: ierror, iostat, i, j, a
CHARACTER(len=50) :: indexfile, output
! Get index list filename
WRITE (*,*) "The atom index file must be an ordered list of atom numbers, one per line,"
WRITE(*,*) "with the first line being the number of atoms involved."
WRITE (*,*) "Enter the name of the file containing the ordered list of atom indices corresponding to matrix data points:"
READ (*,*), indexfile
! Read the atom indices and put them into a 2D array for (x,y)
OPEN (UNIT=10, FILE=indexfile, STATUS='OLD', ACTION='READ', IOSTAT=ierror)
READ (10,*) a
ALLOCATE (atomnumbers(1:a), STAT=iostat)
WRITE (*,*) "Reading indices..."
DO i = 1, a, 1
   READ (10,'I5') atomnumbers(i)
END DO
CLOSE (UNIT=10)
! Allocate data array
ALLOCATE (covar(1:a, 1:a), STAT=iostat)
! Fill data array
OPEN (UNIT=20, FILE='covar.matrix', STATUS='OLD', ACTION='READ', IOSTAT=ierror)
! Loops to read in the input data into matrix "array"
WRITE (*,*) "Reading covariance values..."
READ (20,*) (( covar(i,j), j=1,i), i=1,a )
!   IF ( MODULO(i,100) == 0 ) THEN
!      WRITE (*,*) i
!   END IF
! Close input file
CLOSE (UNIT=20)
! Get window limits from user
WRITE (*,*) 'What is the lower covariance limit you would like for output (decimal)?'
READ (*,*) lowbin
WRITE (*,*) 'What is the upper covariance limit you would like for output (decimal)?'
READ (*,*) highbin
! Open file for output
WRITE (*,*) 'Enter filename for output:'
READ (*,*) output
OPEN (UNIT=100, FILE=output, STATUS='NEW', ACTION='WRITE', IOSTAT=ierror)
! Dump data in "array" in Gaussian fchk format
WRITE (100,*) 'Atom 1  Atom 2    Covariance'
DO i = 1, a, 1
   DO j = 1, a, 1
      IF ( (covar(i,j) <= highbin) .AND. (covar(i,j) >= lowbin) ) THEN
         WRITE (100,'2I7,F12.3') atomnumbers(i), atomnumbers(j), covar(i,j)
      ENDIF
   END DO
END DO
CLOSE (UNIT=100)
DEALLOCATE (atomnumbers, STAT=iostat)
DEALLOCATE (covar, STAT=iostat)
END PROGRAM COVA_SORT
