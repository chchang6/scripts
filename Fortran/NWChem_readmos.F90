PROGRAM nwchem_read_mos
! Program to read NWChem molecular orbital vector files and 
! create a formatted file. Vector replacements can be done here,
! and the binary file re-created for e.g., NBO initial guesses.
! CHC March, 2007.
implicit none
!
!     Temporary routine
!
character(len=30) :: oldfile, newfile ! [input] Filenames for conversion
character :: title       ! [input] Title of job that created vectors
integer :: nbf               ! No. of functions in basis
integer :: nsets             ! No. of sets of vectors
integer,dimension(2) :: nmo        ! No. of vectors in each set
real(kind=8),allocatable,dimension(:) :: occ, evals, dbl_mb ! Occupations, 
! eigenvalues, MO coefficients 
integer :: lentit
integer :: lenbas
integer :: k_vecs
integer :: ierror, iset, i, j
character(len=26) :: date
character(len=32) :: geomsum, basissum ! Checksums
character(len=20) :: scftype20 ! Shortened version of scftype
character :: basis_name ! Name of basis, usually "ao basis"
real(kind=8) :: energy, enrep
!
write(*,*) 'Enter name of binary file to read:'
read(*,*) oldfile
write(*,*) 'Enter name of formatted file to create:'
read(*,*) newfile
open(unit=67, status='old', action='read', form='unformatted', &
     file=oldfile, iostat=ierror)
open(unit=10, file=newfile, status='new', action='write', &
     form='formatted', iostat=ierror)
!
!     Information about convergence
!
read(67, iostat=ierror) basissum, geomsum, scftype20, date
write(10,100) basissum
100 FORMAT ('basissum=',A32)
write(10,101) geomsum
101 FORMAT ('geomsum=',A32)
write(10,102) scftype20
102 FORMAT ('scftype20=',A20)
write(10,103) date
103 FORMAT ('date =',A26)
!
!     Check that read routines are both consistent with this
!
read(67, iostat=ierror) scftype20
!        lentit = max(1,inp_strlen(title)) ! 0 length record confuses f2c
read(67, iostat=ierror) lentit
write(10,104) lentit
104 FORMAT('Title length is ', I3)
read(67, iostat=ierror) title(1:lentit)
write(10,105) title(1:lentit)
105 FORMAT('Title is "',A,'"')
lenbas = max(1,len(basis_name))
read(67, iostat=ierror) lenbas
write(10,106) lenbas
106 FORMAT('Length of basis name is ',I2)
read(67, iostat=ierror) basis_name(1:lenbas)
write(10,107) basis_name(1:lenbas)
107 FORMAT('Basis name is " ',A,'"')
read(67, iostat=ierror) nsets
write(10,108) nsets
108 FORMAT('Number of vector sets is ', I1)
read(67, iostat=ierror) nbf
write(10,109) nbf
109 FORMAT('Number of basis functions is ',I4)
read(67, iostat=ierror) nmo(1:nsets)
do i = 1, nsets
   write(10,110) i, nmo(i)
   110 FORMAT('Number of vectors in set ',I1,' is',I4)
end do
! Read in occupation number and eigenvalue arrays
allocate (occ(nmo(1))) ! Note: if there are different numbers
! of occupation numbers or evals, have to write routine to find max.
allocate (evals(nmo(1)))
allocate (dbl_mb(nbf))
do iset = 1, nsets
   read(67, iostat=ierror) (occ(j),j=1,nmo(iset))
   write(10,*) 'Occupation numbers'
   write(10,'(10F8.5)') (occ(j),j=1,nmo(iset))
   write(10,*)
   read(67, iostat=ierror) (evals(j),j=1,nmo(iset))
   write(10,*) 'Eigenvalues'
   write(10,'(3F24.16)') (evals(j),j=1,nmo(iset))
   write(10,*)
   write(10,*) 'MO vectors'
   do i = 1, nmo(iset)
      k_vecs=1
      read(67, iostat=ierror) (dbl_mb(k_vecs+j), j=0,nmo(iset)-1)
      write(10,111) i
      111 FORMAT(I5)
      write(10,112) dbl_mb
      112 FORMAT(4D20.14)
   enddo
enddo
deallocate (occ, STAT=ierror)
deallocate (evals, STAT=ierror)
!
! Read scf energy at the end of the movecs file. If energy
! is not in rtdb, it's given a value of zero.
!
read(67, iostat=ierror) energy, enrep
write(10,113) energy
113 FORMAT('SCF energy is ',F18.12,' Ha')
write(10,114) enrep
114 FORMAT('Nuclear repulsion energy is ',F18.12,' Ha')
close(67,iostat=ierror)
close(10,iostat=ierror)
END PROGRAM nwchem_read_mos
