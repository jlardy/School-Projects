program indexArray
	! This program reads in a file to an array to be sorted through idexing.
	! The subroutine createIndexArr is passed an unsorted array along with an 
	! initialized array of indexes the length of the array to be sorted and 
	! returns a sorted index array as keys to the original array.
	
    implicit none
   
    ! Declare variables
    integer :: n, i
    real, allocatable :: inputValues(:)
	integer, allocatable:: indexArray(:)
    character*50:: fileName
    logical :: Success
   
   
	! get read the file 
    print*, 'Please enter a file path: '
    read(*,*) fileName
    open(42,file=fileName)
	open(43,file='output.txt')

    ! number of lines
    read(42,*) n
	
	! allocate arrays for read in values and idexing
    allocate(inputValues(n), indexArray(n))
   
	! read in values and initialize indexArray values 1-n
	do i = 1, n
		read(42, *) inputValues(i)
		indexArray(i) = i
	enddo
	
	! call the createIndexArr subroutine 
	call createIndexArr(inputValues, n, indexArray)
	
	! write the sorted array to a new file using idexing
	write(43,*) n
	do i = 1, n
		write(43,*) inputValues(indexArray(i))
	enddo
   
	! deallocate arrays
    deallocate(inputValues, indexArray)  
	
	! close files
	close(42)
	close(43)

	! show the program is complete
	print*,'Done!'
end program indexArray


! bubble sort indexing 
subroutine createIndexArr(valuesArr, n, indexArray)
integer:: n, i, j, indexArray(n)
real:: valuesArr(n)
logical:: done

do i = 1,n-1
	done = .true.
	do j = 1, n-i
		if(valuesArr(indexArray(j)) .gt. valuesArr(indexArray(j+1))) then
			temp = indexArray(j)
			indexArray(j) = indexArray(j+1)
			indexArray(j+1) = temp
			done = .false.
		endif
	enddo
	if(done) exit
enddo

endsubroutine createIndexArr
