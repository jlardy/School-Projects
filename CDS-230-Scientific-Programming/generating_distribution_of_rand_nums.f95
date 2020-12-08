program randomDistributedNumbers
	! The purpose of this program is to generate normally distributed random numbers based off of a certain mean 
	! and standard deviation. The output of this program is stored in a text file called bumps.txt
   	implicit none
	double precision:: avg, std, boxMuller
	integer:: i, n, seed
	
	! Initialize the random function
	print*, "Please enter a seed in integer form : "
	read(*,*) seed	
	call srand(seed)
	
	! open an output file
	open(43, file='Bumps.txt')
	
	! write the first part of the file with an average of 22 and standard dev of 2.5
	do i=1,13000
		write(43, *) boxMuller(22.d0, 2.5d0)
	enddo
	
	! write the second part of the file with an average of 15.5 and standard dev of 1.0
	do i=1,7000
		write(43, *) boxMuller(15.5d0, 1.d0)
	enddo
	
	print*, 'Done!'
end program randomDistributedNumbers

function boxMuller(avg, std) result(rNum)
	! helper function to main program. This function converts a random linear number into a guassian distributed number.
	! returns one random number. 
	implicit none
	double precision:: avg, std , x1, x2, w, rNum
	do 
		x1 = 2.d0 * rand() - 1.d0
		x2 = 2.d0 * rand() - 1.d0
		w = x1**2 + x2**2
		if(w .lt. 1.d0) exit
	enddo
	w = sqrt((-2.d0 * log(w))/w)
	rNum = x1 * w
	rNum = rNum * std + avg
end function boxMuller
