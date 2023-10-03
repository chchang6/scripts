PROGRAM NHONBO_guess
! Program reads in a single ordered list of orbital types from file,
! then assembles an NWChem movecs input deck in 4D20.14 for initial
! guess based on NBOs and NHOs. CHC 04/24/07.
IMPLICIT NONE
INTEGER, ALLOCATABLE, DIMENSION (:) :: input_orbnum
REAL, ALLOCATABLE, DIMENSION (:,:) :: NHO, NBO, output
INTEGER :: ierror, iostat, i, j, numorbs, numbasis
CHARACTER, ALLOCATABLE, DIMENSION (:) :: input_NXOtype
CHARACTER(len=1) :: test
WRITE (*,*) "Required input filenames are NXOlist, AONHO.matrix,"
WRITE (*,*) "and AONBO.matrix. Will output NXO_cards. You must know the number"
WRITE (*,*) "of NXOs and basis functions. OK to proceed (y/n)?"
READ (*,*), test
IF (test /= 'y') STOP

! Get total number of orbitals
WRITE (*,*) "Enter the number of (P)NXOs in NXOlist:"
READ (*,*), numorbs
WRITE (*,*) "Enter the number of basis functions:"
READ (*,*), numbasis
ALLOCATE (input_orbnum (1:numorbs), STAT=iostat)
ALLOCATE (input_NXOtype (1:numorbs), STAT=iostat)
ALLOCATE (NHO(1:numbasis, 1:numbasis), STAT=iostat)
ALLOCATE (NBO(1:numbasis, 1:numbasis), STAT=iostat)

! Read input list from file "NXOlist" into 1-column array "input".
! First column is NXO index; second column is NXO type (A, H, or B).
OPEN (UNIT=9, FILE='NXOlist', STATUS='OLD', ACTION='READ', IOSTAT=ierror)
DO i=1,numorbs
   READ (9,'(I4,A1)') input_orbnum(i), input_NXOtype(i)
END DO
CLOSE (UNIT=9)

! Open files for input and read in data. Each NXO is a block.
OPEN (UNIT=10, FILE='AONHO.matrix', STATUS='OLD', ACTION='READ', IOSTAT=ierror)
READ (10,*)
READ (10,*)
READ (10,*)
READ (10,*)
DO i=1,numbasis
   READ (10,'(5F16.9)') NHO(i,:)
END DO
CLOSE (UNIT=10)

OPEN (UNIT=11, FILE='AONBO.matrix', STATUS='OLD', ACTION='READ', IOSTAT=ierror)
READ (11,*)
READ (11,*)
READ (11,*)
READ (11,*)
DO i=1,numbasis
   READ (11,'(5F16.9)') NBO(i,:)
END DO
CLOSE (UNIT=11)

! Create new array with desired orbitals picked from each file
! Have to change organization from row-NXO to column-NXO due to
! "column-major" output in F90.
ALLOCATE (output(1:numorbs, 1:numbasis), STAT=iostat)
DO j=1,numorbs
   i = input_orbnum(j)
   IF (input_NXOtype(j) == "H") THEN
      output(j,:) = NHO(i,:)
   ELSE IF (input_NXOtype(j) == "B") THEN
      output(j,:) = NBO(i,:)
   ELSE
      WRITE (*,*) "NXO type is not recognized!"
      STOP
   END IF
END DO

DEALLOCATE (input_orbnum, STAT=iostat)
DEALLOCATE (input_NXOtype, STAT=iostat)
DEALLOCATE (NHO, STAT=iostat)
DEALLOCATE (NBO, STAT=iostat)

! Write out Gaussian Cards-formatted orbitals.
OPEN (UNIT=20, FILE='NXO_cards', STATUS='NEW', ACTION='WRITE', IOSTAT=ierror)
DO i=1,numorbs
   WRITE (20,'(i5)') i
   WRITE (20,'(4E20.14)') output(i,:)
END DO
CLOSE (UNIT=20)
DEALLOCATE (output, STAT=iostat)
END PROGRAM
