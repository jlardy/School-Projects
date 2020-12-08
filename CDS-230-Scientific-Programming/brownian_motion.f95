program brownianMotion
	! Program simulates a random walk of a particle for a number of steps dictated b the user. 
	! Writes the x,y coordinates from the random movement to a text file 'brownian.txt'. 
   	implicit none 
	integer:: i, n, seed, x, y
	real:: temp 
	x = 0
	y = 0
	
	! Initialize the random function
	print*, "Please enter a seed in integer form : "
	read(*,*) seed	
	call srand(seed)
	
	! get the number of steps
	print*, "Please enter the number of desired steps in integer form : "
	read(*,*) n	
	
	! open an output file
	open(43, file='brownian.txt')
	
	! loop until for the desired amount of steps and add to an x,y based off a random number
	do i=1, n
		write(43, *) x, y
		temp = rand()
		if(temp .lt. .25) then 
			x = x + 1
		else if(temp .lt. .50) then 
			y = y + 1
		else if(temp .lt. .75) then 
			x = x - 1
		else
			y = y - 1
		endif 
	enddo
	
	! close files and show the program is done
	close(43)
	print*, 'Done!'
end program brownianMotion


