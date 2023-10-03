PROGRAM NAONHONBO_guess
! Program reads in a single ordered list of orbital types from file,
! then assembles formchk-format coefficient array to generate an initial
! guess based on NBOs, NHOs, and NAOs. CHC 12/08/05.
IMPLICIT NONE
INTEGER, ALLOCATABLE, DIMENSION (:) :: input_orbnum
REAL, ALLOCATABLE, DIMENSION (:,:) :: NAO, NHO, NBO, output
INTEGER :: ierror, iostat, i, j, num
CHARACTER, ALLOCATABLE, DIMENSION (:) :: input_NXOtype
CHARACTER(len=1) :: test
WRITE (*,*) "Required input filenames are NXOlist, AONAO.matrix, AONHO.matrix,"
WRITE (*,*) "and AONBO.matrix. Will output NXO_fchk. OK to proceed (y/n)?"
READ (*,*), test
IF (test /= 'y') STOP

! Get total number of orbitals
WRITE (*,*) "Enter the number of (P)NXOs:"
READ (*,*), num
ALLOCATE (input_orbnum (1:num), STAT=iostat)
ALLOCATE (input_NXOtype (1:num), STAT=iostat)
ALLOCATE (NAO(1:num, 1:num), STAT=iostat)
ALLOCATE (NHO(1:num, 1:num), STAT=iostat)
ALLOCATE (NBO(1:num, 1:num), STAT=iostat)

! Read input list from file "NXOlist" into 1-column array "input".
! First column is NXO index; second column is NXO type (A, H, or B).
OPEN (UNIT=9, FILE='NXOlist', STATUS='OLD', ACTION='READ', IOSTAT=ierror)
DO i=1,num
   READ (9,'I4,A1') input_orbnum(i), input_NXOtype(i)
END DO
CLOSE (UNIT=9)

! Open files for input and read in data. Each NXO is a block.
OPEN (UNIT=10, FILE='AONAO.matrix', STATUS='OLD', ACTION='READ', IOSTAT=ierror)
READ (10,*)
READ (10,*)
READ (10,*)
DO i=1,num
   READ (10,'5F16.9') NAO(i,:)
END DO
CLOSE (UNIT=10)

OPEN (UNIT=11, FILE='AONHO.matrix', STATUS='OLD', ACTION='READ', IOSTAT=ierror)
READ (11,*)
READ (11,*)
READ (11,*)
READ (11,*)
DO i=1,num
   READ (11,'5F16.9') NHO(i,:)
END DO
CLOSE (UNIT=11)

OPEN (UNIT=12, FILE='AONBO.matrix', STATUS='OLD', ACTION='READ', IOSTAT=ierror)
READ (12,*)
READ (12,*)
READ (12,*)
READ (12,*)
DO i=1,num
   READ (12,'5F16.9') NBO(i,:)
END DO
CLOSE (UNIT=12)

! Create new array with desired orbitals picked from each file
! Have to change organization from row-NXO to column-NXO due to
! "column-major" output in F90.
ALLOCATE (output(1:num, 1:num), STAT=iostat)
DO j=1,num
   i = input_orbnum(j)
   IF (input_NXOtype(j) == "A") THEN
      output(:,j) = NAO(i,:)
   ELSE IF (input_NXOtype(j) == "H") THEN
      output(:,j) = NHO(i,:)
   ELSE IF (input_NXOtype(j) == "B") THEN
      output(:,j) = NBO(i,:)
   ELSE
      WRITE (*,*) "NXO type is not recognized!"
      STOP
   END IF
END DO

DEALLOCATE (input_orbnum, STAT=iostat)
DEALLOCATE (input_NXOtype, STAT=iostat)
DEALLOCATE (NAO, STAT=iostat)
DEALLOCATE (NHO, STAT=iostat)
DEALLOCATE (NBO, STAT=iostat)

! Write out Gaussian fchk-formatted orbitals.
OPEN (UNIT=20, FILE='NXO_fchk', STATUS='NEW', ACTION='WRITE', IOSTAT=ierror)
WRITE (20,'5E16.8') output(:,:)
CLOSE (UNIT=20)
DEALLOCATE (output, STAT=iostat)
END PROGRAM
