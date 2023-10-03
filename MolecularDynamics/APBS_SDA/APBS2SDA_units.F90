PROGRAM apbs2sda
! Program converts the electrostatic potential values from APBS (kT/e)
! in UHBD ASCII format to same format in SDA input units (kcal/mol/e)
! CHC, 5/27/05

IMPLICIT NONE

! TYPE DECLARATIONS
INTEGER :: gridx, gridy, gridz, z, numvalues, ierror, status, i
CHARACTER(len=72) :: header
REAL, ALLOCATABLE, DIMENSION(:) :: grid_in, grid_out

! Open input file, named by ESP.uhbd
WRITE (6,*) 'Input file is assumed to be ESP.uhbd'
WRITE (6,*) 'Output file will be ESP.sda'
WRITE (6,*) 'Enter 1 to continue, 0 to abort'
READ (5,*) status
IF (status == 0) STOP 'Terminated by user input'
OPEN (UNIT=8, FILE='ESP.uhbd', ACTION='READ', IOSTAT=ierror)

! Read through first two lines, then grab grid dimensions
READ (8,*)
READ (8,*)
READ (8,100) gridx, gridy, gridz
100 FORMAT (3I7)

! Array dimension is number of points in grid
numvalues=gridx*gridy
! Go back, dump out first 7 lines, then multiply array by conversion
! factor and dump out to output file, named "ESP.sda"
REWIND (UNIT=8)
OPEN (UNIT=9, FILE='ESP.sda', ACTION='WRITE')
DO i = 1, 5
   READ (8,'(A72)') header
   WRITE (9,'(A72)') header
ENDDO
ALLOCATE (grid_in(numvalues), STAT=status)
ALLOCATE (grid_out(numvalues), STAT=status)
DO i = 1, gridz
   READ (8, 100) z,gridy,gridx
   READ (8, 110) grid_in
   grid_out=0.5961*grid_in
   WRITE (9, 100) z,gridy,gridx
   WRITE (9, 110) grid_out
ENDDO
110 FORMAT (6ES13.5)
DEALLOCATE (grid_in, grid_out, STAT=status)
CLOSE (UNIT=8)
CLOSE (UNIT=9)
END PROGRAM
