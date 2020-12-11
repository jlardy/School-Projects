program quick

    implicit none
	! The purpose of this program is to implement the quicksort algorithm. When executed, user is 
	! prompted to enter a filepath to a text file to be sorted. The text file must have to number of
	! entries as the first line. If the file is already sorted the program will exit. Only sorts ascending.
   
    ! Declare varialbles
    integer :: n, i, partition
    real, allocatable :: inputValues(:)
    character*50:: fileName
	logical:: checkSorted
   
    print*, 'Please enter a file path: '
    read(*,*) fileName
    open(42,file=fileName)
	open(43,file='output.txt')

    ! read in unsorted file 
    read(42,*) n
    allocate(inputValues(n))
 
	do i = 1, n
		read(42, *) inputValues(i)
	enddo
	
	! Check if the array needs to be sorted or not
	if(checkSorted(inputValues, n)) then 
		print*, 'Array is already sorted!'
	else
		print*, 'Sorting...'
		call quickSort(inputValues, n, 1, n)
		
		! write sorted values to file
		write(43,*) n
		do i = 1, n
			write(43,*) inputValues(i)
		enddo
	endif
   
	! deallocate all arrays 
    deallocate(inputValues)  
   
    ! close files
    close(42)
    close(43)
	print*, 'Done!'
end program quick


recursive subroutine quickSort(valuesArr, n, lo, hi)
	! Recursive subroutine to efficiently sort an unsorted array 
	! Needs helper function partition to work correctly
	integer:: n, p, hi, lo, partition
	real:: valuesArr(n)
	
	if(lo .lt. hi) then
		p = partition(valuesArr, n , lo, hi)
		call quickSort(valuesArr, n, lo, p-1)
		call quickSort(valuesArr, n, p+1, hi)
	endif
endsubroutine quickSort

function partition(Arr, n, lo, hi) result(p)
	! Helper function for recursive quick sort subroutine. In one pass it checks if any value 
	! is smaller than the value at the end of the list (pivot) sent to it. Returns the end position 
	! of the pivot along with partially sorting the array. 
	integer:: n, hi, lo, p, i
	real:: Arr(n), pivot, temp
	
	p = lo
	pivot = Arr(hi)
	do i = lo, hi-1
		if(Arr(i) .le. pivot) then 
			temp = Arr(p)
			Arr(p) = Arr(i)
			Arr(i) = temp
			p = p + 1
		endif
	enddo
	
	temp = Arr(p)
	Arr(p) = pivot
	Arr(hi) = temp 
end function partition

function checkSorted(Arr, n) result(sorted)
	! Function to check if an array is already sorted, prescreen for the quicksort algorithm.
	! Assumes that array is sorted ascending. 
	integer:: n, i
	real:: Arr(n)
	logical:: sorted
	sorted = .True.
	
	! If any previous value is larger than the next value array is unsorted and returns false
	do i = 1, n-1
		if(Arr(i) .GT. Arr(i+1)) then 
			sorted = .False.
			exit
		endif
	enddo
endfunction checkSorted
