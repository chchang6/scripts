PROGRAM CHARMM_temper_ener_extr
! Program extracts the total energy and temperatures from energies file
! created during a CHARMM dynamics run.
! CHC, 6/07/05

IMPLICIT NONE

! TYPE DECLARATIONS
INTEGER :: numpoints, status, ierror, i
REAL :: time, tote, temp

! Open input file, named by ESP.uhbd
WRITE (6,*) 'Input file is assumed to be energies'
WRITE (6,*) 'Output file will be tempener.gnu for GNUplot'
WRITE (6,*) 'Enter 1 to continue, 0 to abort'
READ (5,*) status
IF (status == 0) STOP 'Terminated by user input'
OPEN (UNIT=8, FILE='energies', ACTION='READ', IOSTAT=ierror)

! Read through first five lines
DO i = 1, 5
READ (8,*)
ENDDO

! Get number of points to read and timestep from user
WRITE (6,*) 'Enter number of points to read in:'
READ (5,*) numpoints
OPEN (UNIT=9, FILE='tempener.gnu', ACTION='WRITE', IOSTAT=ierror)
DO i = 1, numpoints
   READ (8,100) time, tote, temp
100 FORMAT (16X,2F16.4,/,16X,F16.4)
   WRITE (9,110) time,tote,temp
110 FORMAT (3F16.4)
   READ (8,*)
   READ (8,*)
ENDDO

CLOSE (UNIT=8)
CLOSE (UNIT=9)
END PROGRAM
