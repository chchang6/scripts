PROGRAM VIBRAN_entropy
! Program to calculate entropic contribution from vibrational
! frequencies calculated using CHARMM VIBRAN module.
! User input is the number of frequencies and temperature
! File input is the output deck from VIBRAN
! Program searches for unique text pattern, backspaces, then
! reads in frequencies in wavenumbers, converts to Hz, and calculates
! TS_vib according to Noskov & Lim, Biophys. J. 81: 737.

IMPLICIT NONE

! Declare variables and data structures
INTEGER :: go, numfreqs, ierror, arrstat, i
CHARACTER(len=15) :: search, infile, outfile
REAL :: kB, h, temp, sum = 0
REAL, ALLOCATABLE, DIMENSION(:) :: wavenum, Hz, entropy

! Constants
kB = 1.3806505E-26   ! Units kiloJoules/Kelvin
h = 6.626E-37        ! Units kiloJoules*seconds

! User warnings and information
WRITE (*,*) "This program will ask you for the total number of frequencies,"
WRITE (*,*) "desired temperature, and the input and output filenames."
WRITE (*,*) "If you don\'t know these, enter 0; otherwise, enter something else:"
READ (*,*) go
IF (go == 0) THEN
   STOP
END IF

! Get user input for temperature and number of frequencies
WRITE (*,*) "What is the maximum frequency index at the end of the"
WRITE (*,*) "CHARMM input file, i.e. don\'t worry about missing 6 transrots)?"
READ (*,*) numfreqs
WRITE (*,*) "At what temperature (Kelvin) should the entropy be calculated?"
READ (*,*) temp
WRITE (*,*) "What is the input filename?"
READ (*,*) infile
WRITE (*,*) "What is the output filename?"
READ (*,*) outfile

! Allocate arrays
ALLOCATE (wavenum(numfreqs-6), STAT=arrstat)
ALLOCATE (Hz(numfreqs-6), STAT=arrstat)
ALLOCATE (entropy(numfreqs-6), STAT=arrstat)

! Read in frequencies
OPEN (UNIT=10, FILE=infile, STATUS='OLD', ACTION='READ', IOSTAT=ierror)
DO
   READ (10,100) search
100  FORMAT (1X,14A)
   IF (search == "VIBRAN>    END") EXIT
END DO
DO i = 1, numfreqs + 4, 1
   BACKSPACE (UNIT=10)
END DO
DO i = 1, numfreqs - 6, 1
   READ (10,110) wavenum(i)
110  FORMAT (13X,F9.4)
   Hz(i) = wavenum(i) * 2.99792458E+10
   entropy(i) = 6.022E+23*((h * Hz(i))/(EXP(h*Hz(i)/kB/temp) - 1) - kB*temp*LOG(1-EXP(-h*Hz(i)/kB/temp)))
   sum = sum + entropy(i)
END DO

CLOSE (UNIT=10)

! Output data to outfile
OPEN (UNIT=20, FILE=outfile, STATUS='NEW', ACTION='WRITE', IOSTAT=ierror)
WRITE (20,*) 'Temperature (degrees K): ', temp
WRITE (20,*) ' Index    cm-1         s-1      TS_vib(kJ/mol)'
DO i = 1, numfreqs-6, 1
   WRITE (20, 120) i, wavenum(i), Hz(i), entropy(i)
120 FORMAT (I5,2X,F9.4,2ES15.6)
END DO
WRITE (20,'(34X,A12)') "------------"
WRITE (20,'(21X,A10,ES15.6)') "Sum =",sum
CLOSE (UNIT=20)

DEALLOCATE (wavenum, Hz, entropy)

END PROGRAM
