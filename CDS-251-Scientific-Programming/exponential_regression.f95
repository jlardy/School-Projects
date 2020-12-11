program exponentialRegression
   ! THIS PROGRAM SOLVES EXPONENTIAL REGRESSION FOR A FILE WITH DATA 
   ! STORED IN X, Y ON EACH LINE 
   ! PRINTS THE RESULTING VALUES FOR THE EQUATION OF BEST FIT AFTER READING 
   ! ALL THE DATA. 
   ! FORM FOR USING THE RESULTS:
   ! Y = A * EXP(B * X-vals)
   implicit none
   
   integer*4 :: i, n
   real :: meanX, meanY, x, y, sxxi, sxyi, b, m
   open(42, file='EData.txt')
   
   ! initialize variables
   n = 200 !num lines
   meanX = 0.
   meanY = 0.
   sxxi = 0.
   sxyi = 0.
   
   ! read in each line of the file and compute 
   do i = 1, n
	read(42, *) x, y
	y = log(y)
	!figure out the S variable
	sxxi = sxxi + ((float(i-1)/float(i)) * (x - meanX)**2)
	sxyi = sxyi + ((float(i-1)/float(i)) * ((x - meanX)*(y-meanY)))
	
	!new meanX and meanY
	meanX = meanX + ((x - meanX)/float(i))
	meanY = meanY + ((y- meanY)/float(i))
	
   enddo
   
   m = sxyi/sxxi
   b = meanY-((sxyi/sxxi)*meanX)
   
   print*, 'A = ', m
   print*, 'B = ', exp(b)

   close(42)
   
   print*, 'Done!'
end program exponentialRegression

