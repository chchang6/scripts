PROGRAM nwchem_write_mos
! Program to write NWChem molecular orbital vector files from
! formatted file with NBO replacements.
! CHC April, 2007.
implicit none
!
!     Temporary routine
!
character(len=30) :: oldfile, newfile     ! [input] Formatted and unformatted filenames
character(len=100) :: title
!Debug character(len=50) :: test1 ! Eigenvalues label
!Debug character(len=50) :: test2 ! Occupation number label
integer(kind=8) :: nbf               ! No. of functions in basis
integer(kind=8) :: nsets             ! No. of sets of vectors
integer(kind=8) :: MOindex           ! MO index
integer(kind=8),allocatable,dimension(:) :: nmo        ! No. of vectors in each set
real(kind=8),allocatable,dimension(:) :: occ, evals, dbl_mb ! Occupations, 
! eigenvalues, MO coefficients 
integer(kind=8) :: lentit,lenbas,ierror,iset,i,j
character(len=26) :: date
character(len=32) :: geomsum, basissum ! Checksums
character(len=20) :: scftype20 ! Shortened version of scftype
character(len=20) :: basis_name ! Name of basis, usually "ao basis"
real(kind=8) :: energy, enrep
!
write(*,*) 'Enter name of formatted file to convert:'
read(*,*) oldfile
write(*,*) 'Enter name of binary file to create:'
read(*,*) newfile
open(UNIT=67, status='old', action='READ', form='formatted', &
     file=oldfile, iostat=ierror)
open(UNIT=10, file=newfile, status='new', action='WRITE', &
     form='unformatted', iostat=ierror)
!
!     Information about convergence
!
read(67,'(9X,A32)') basissum
read(67,'(8X,A32)') geomsum
read(67,'(10X,A20)') scftype20
read(67,'(6X,A26)') date
write(10) basissum, geomsum, scftype20, date
!
write(10) scftype20
read(67,'(16X,I3)') lentit
write(10) lentit
!Debug write(*,'(A21,I3)') "Title length =", lentit
read(67,'(10X,A)') title(1:lentit)
write(10) title(1:lentit)
read(67,'(24X,I2)') lenbas
write(10) lenbas
read(67,'(16X,A)') basis_name(1:lenbas)
write(10) basis_name(1:lenbas)
read(67,'(25X,I1)') nsets
write(10) nsets
!Debug write(*,100) nsets
!Debug 100 FORMAT('Number of vector sets is ', I2)
read(67,'(29X,I4)') nbf
write(10) nbf
!Debug write(*,101) nbf
!Debug 101 FORMAT('Number of basis functions is ', I5)
!
allocate (nmo(nsets))
do i = 1, nsets
   read(67,'(29X,I4)') nmo(i)
!Debug   write(*,102) i, nmo(i)
!Debug 102 FORMAT('Number of vectors in set ', I1, ' is ', I5)
end do
write(10) (nmo(i),i=1,nsets)
! Occupation number and eigenvalue arrays
allocate (occ(nmo(1))) ! Note: if there are different numbers
! of occupation numbers or evals, have to write routine to find max.
allocate (evals(nmo(1)))
allocate (dbl_mb(nbf))
do iset = 1, nsets
   read(67,*) ! "Occupation numbers" label
!Debug   read(67,*) test2
!Debug   write(*,'(A50)') test2
   read(67,'(10F8.5)') (occ(j),j=1,nmo(iset))
   write(10) occ
   read(67,*) ! Blank line after ON table
   read(67,*) ! "Eigenvalues" label
!Debug   read(67,*) test1 ! "Eigenvalues" label
!Debug   write(*,'(A50)') test1
   read(67,'(3F24.16)') (evals(j),j=1,nmo(iset))
   write(10) evals
   read(67,*) ! Blank line after EV table
   read(67,*) ! "MO vectors" label
!Debug   write(*,'(I5)') nmo(iset)
   do i = 1, nmo(iset)
      read(67,*) ! MO index
!Debug      read(67,'(I5)') MOindex
!Debug      write(*,'(I5)') MOindex
      read(67,'(4D20.14)') ( dbl_mb(j), j = 1, nmo(iset) )
      write(10) dbl_mb
   enddo
enddo
deallocate (occ, STAT=ierror)
deallocate (evals, STAT=ierror)
deallocate (dbl_mb, STAT=ierror)
deallocate (nmo, STAT=ierror)
!
! Read scf energy at the end of the movecs file. If energy
! is not in vectors file or exceeds field width, it's given a value of zero.
!
read(67,'(14X,F18.12)',ERR=200) energy
200 energy = 0.0
read(67,'(28X,F18.12)') enrep
write(10) energy, enrep
close(67,iostat=ierror)
close(10,iostat=ierror)
END PROGRAM nwchem_write_mos
