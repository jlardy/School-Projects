program quadRegression
   ! THIS PROGRAM SOLVES QUADRATIC REGRESSION FOR DATA STORED IN A TEXT FILE AS 
   ! X,Y PAIRS ON THE SAME LINE AND PRINTS TO THE TERMINAL THE COEFFICIENTS AND 
   ! CONSTANTS AS A, B, AND C
   !
   ! FORM FOR USING THE RESULTS:
   ! Y-val = (A * X-val^2) + (B * X-val) + C 
   implicit none
   
   integer*4 :: i, n
   real :: meanX, meanY, x, y, sxx, sxy, a, b, c, sx2x2, sxx2, sx2y, meanX2
   ! open the textfile
   open(42, file='QuadData.txt')
   
   !initialize all the variables 
   n = 200 !num lines
   meanX = 0.
   meanY = 0.
   meanX2 = 0.
   sxx = 0.
   sxy = 0.
   sx2x2 = 0.
   sxx2 = 0.
   sx2y = 0.
   
   !read in data one line at a time
   do i = 1, n
	read(42, *) x, y
	
	!figure out the S varaibles line by line
	sxx = sxx + ((float(i-1)/float(i)) * ((x - meanX)**2))
	sxy = sxy + ((float(i-1)/float(i)) * ((x - meanX)*(y-meanY)))
	sxx2 = sxx2 + ((float(i-1)/float(i)) * ((x - meanX)*((x**2) - (meanX2))))
	sx2x2 = sx2x2 + ((float(i-1)/float(i)) * (((x**2) - (meanX2))**2))	
	sx2y = sx2y +  ((float(i-1)/float(i)) * ((y-meanY)*((x**2) - (meanX2))))	
	
	!new meanX and meanY
	meanX = meanX + ((x - meanX)/float(i))
	meanX2 = meanX2 + ((x**2 - meanX2)/float(i)) !note the mean squared does not equal the actual mean squared
	meanY = meanY + ((y- meanY)/float(i))
	
   enddo
   
   ! a is the unknown coefficient for x2
   a = (((sx2y*sxx) - (sxy*sxx2)) / ((sxx * sx2x2) - (sxx2**2)))
   ! b is the unknown coefficient for x
   b = (((sxy*sx2x2) - (sx2y*sxx2)) / ((sxx*sx2x2) - (sxx2**2)))
   ! c is the constant
   c = (meanY - (b*meanX) - (a*meanX2))
   
   print*, 'x^2 coefficient A = ', a
   print*, 'x coefficient B = ', b
   print*, 'Constant C = ', c
   print*, meanX, meanX2
   ! close the opened files
   close(42)
   
   ! show the program is done
   print*, 'Done!'
end program quadRegression

